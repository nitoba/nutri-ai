from chatbot.telegram import TelegramBot
from graph_builder import agent_graph

bot = TelegramBot(agent=agent_graph)

if __name__ == '__main__':
    bot.run()
