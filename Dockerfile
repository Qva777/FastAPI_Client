FROM python:3.8

#RUN  pip install --upgrade pip
WORKDIR /appfolder
RUN pip install pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["echo SECRET_KEY=YOUR_SECRET_KEY > .env", "uvicorn main:app --reload"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
