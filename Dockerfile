FROM python:3.8
#3.8-alpine
#LABEL "name"="Qva777"


WORKDIR /app
RUN pip install pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN echo SECRET_KEY=YOUR_SECRET_KEY > .env

COPY . .
#CMD ["echo", "SECRET_KEY=YOUR_SECRET_KEY >", ".env"]
#CMD echo SECRET_KEY=YOUR_SECRET_KEY > .envuvicorn main:app --reload
ENTRYPOINT echo SECRET_KEY=YOUR_SECRET_KEY > .env
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--reload"]
EXPOSE 8000
#ENTRYPOINT uvicorn main:app --host 127.0.0.0 --port 8000 --reload

