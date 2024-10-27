FROM python:3.12.4-slim AS build

COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get install -y libpq-dev gcc && python3 -m venv /venv

ENV PATH=/venv/bin:$PATH

RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.12.4-slim AS runtime

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH


# Definir variáveis de ambiente
ENV API_KEY=your_open_ai_key
ENV TELEGRAM_API_ID=test
ENV TELEGRAM_API_HASH=test
ENV TELEGRAM_TOKEN=asd


WORKDIR /app

COPY . .

ENTRYPOINT ["python3", "src/app.py"]
