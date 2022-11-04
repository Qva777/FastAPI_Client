#FROM python:3.8
##3.8-alpine
##LABEL "name"="Qva777"
#
#
#WORKDIR /app
#RUN pip install pip
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
##RUN echo SECRET_KEY=YOUR_SECRET_KEY > .env
#EXPOSE 8000
#
#COPY . .
##CMD ["echo", "SECRET_KEY=YOUR_SECRET_KEY >", ".env"]
##CMD echo SECRET_KEY=YOUR_SECRET_KEY > .envuvicorn main:app --reload
##ENTRYPOINT echo SECRET_KEY=YOUR_SECRET_KEY > .env
##CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--reload"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

#ENTRYPOINT uvicorn main:app --host 127.0.0.0 --port 8000 --reload

FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*s

WORKDIR /code

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

EXPOSE 8000

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]