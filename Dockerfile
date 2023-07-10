FROM python

COPY . /
WORKDIR /
COPY vars.py /
COPY gsheet.py /


RUN pip install pyTelegramBotAPI
RUN pip install psycopg2
RUN pip install redis
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN pip install python-dateutil

CMD ["python", "bot.py"]    