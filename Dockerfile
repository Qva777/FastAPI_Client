FROM python:3.8
#3.8-alpine
LABEL "name"="I'm author prod"
#RUN apk update && apk upgrade && apk add bash

# Main directory
WORKDIR /app
# Run install pip and libraries
RUN pip install pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Create secret key
RUN echo SECRET_KEY=YOUR_SECRET_KEY > .env
COPY . .
# Point the port
EXPOSE 8000
# Up server on localhost
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000 --reload

