import asyncio
import logging
import os

from langgraph.graph.state import CompiledStateGraph
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from env import env


class TelegramBot:
    def __init__(self, agent: CompiledStateGraph):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
        )
        self.logger = logging.getLogger(__name__)

        self.app = Client(
            name='Nutri[AI]',
            api_id=env.TELEGRAM_API_ID,
            api_hash=env.TELEGRAM_API_HASH,
            bot_token=env.TELEGRAM_TOKEN,
        )

        self._setup_handlers()
        self.agent = agent

    def _setup_handlers(self):
        start_handler = MessageHandler(
            self.start, filters=filters.command('start') & filters.private
        )
        self.app.add_handler(start_handler)

        # Handler para mensagens de texto
        text_filter = filters.text & filters.private
        message_handler = MessageHandler(self.handle_message, text_filter)
        self.app.add_handler(message_handler)

        # Handler para mensagens de foto
        photo_filter = filters.photo & filters.private
        photo_handler = MessageHandler(self.handle_photo, photo_filter)
        self.app.add_handler(photo_handler)

        self.logger.info('Handlers configurados com sucesso.')

    def run(self):
        self.logger.info('O Nutri[AI] está online!')
        self.app.run()

    async def start(self, client: Client, message: Message):
        self.logger.info(
            f'Usuário [{message.from_user.id}] iniciou uma conversa.'
        )
        await message.reply_text(
            'Olá! Eu sou o Nutri[AI], seu assistente de nutrição. Como posso ajudar? Envie uma mensagem ou uma foto de um alimento para começar.'
        )

    async def handle_message(self, client: Client, message: Message):
        user_id = message.from_user.id
        user_input = message.text
        await client.send_chat_action(
            chat_id=message.chat.id, action=ChatAction.TYPING
        )
        response_message = await message.reply_text(
            'Processando...', parse_mode=ParseMode.MARKDOWN
        )

        try:
            # Analisa se o usuário pediu especificamente o PDF
            pdf_requested = (
                'enviar pdf' in user_input.lower()
                or 'enviar plano' in user_input.lower()
            )

            # Obtenha a resposta do agente
            response = await self.agent.ainvoke(
                {'messages': ('user', user_input)},
                {'configurable': {'thread_id': user_id}},
                debug=True,
            )
            last_message = response['messages'][-1]
            print(last_message)

            # Verifica se o PDF foi gerado e ainda não enviado
            pdf_path = response.get('pdf_path')
            if pdf_requested and pdf_path and os.path.exists(pdf_path):
                # Envia o PDF e marca que já foi enviado
                await client.send_document(
                    chat_id=message.chat.id,
                    document=pdf_path,
                    caption='Aqui está seu plano alimentar em PDF.',
                )
                # Atualiza o estado para indicar que o PDF foi enviado
                response['pdf_sent'] = True
            else:
                # Caso contrário, responde com a mensagem de texto do agente
                await response_message.edit_text(last_message.content)

        except Exception as e:
            self.logger.error(
                f'Erro ao processar mensagem do usuário [{user_id}]: {e}',
                exc_info=True,
            )
            await message.reply_text(
                'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.'
            )
        self.logger.info(f'Resposta enviada para o usuário [{user_id}].')

    async def handle_photo(self, client: Client, message: Message):
        user_id = message.from_user.id
        await client.send_chat_action(
            chat_id=message.chat.id, action=ChatAction.TYPING
        )

        storage_dir = os.path.join(os.getcwd(), 'storage')
        os.makedirs(storage_dir, exist_ok=True)
        photo_file_name = f'{user_id}_{message.photo.file_unique_id}.jpg'
        photo_file_path = os.path.join(storage_dir, photo_file_name)
        await message.download(file_name=photo_file_path)

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.agent.run, photo_file_path
            )
            if not response.strip():
                response = 'Desculpe, não consegui processar sua solicitação. Por favor, tente novamente.'
            await message.reply_text(response)
        except Exception as e:
            self.logger.error(
                f'Erro ao processar imagem do usuário [{user_id}]: {e}',
                exc_info=True,
            )
            await message.reply_text(
                'Desculpe, ocorreu um erro ao processar sua imagem. Por favor, tente novamente.'
            )

        self.logger.info(f'Resposta enviada para o usuário [{user_id}].')
