FROM python:3.13-alpine AS production

WORKDIR /usr/telegram/audio-bot

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . .

RUN yoyo apply --batch --database sqlite:///database.sqlite migrations/

CMD [ "python", "bot.py" ]
