FROM python:3.8
#3.8-alpine
#LABEL "website.name"="geeksforgeeks website"
#LABEL "website.tutorial-name"="docker"
#LABEL website="geeksforgeeks"
#LABEL desc="This is docker tutorial with \
#geeksforgeeks website"
#LABEL tutorial1="Docker" tutorial2="LABEL INSTRUCTION"
#RUN apk update && apk upgrade && apk add bash

WORKDIR /app
RUN pip install pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN echo SECRET_KEY=YOUR_SECRET_KEY > .env

COPY . .
EXPOSE 8000
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000 --reload

