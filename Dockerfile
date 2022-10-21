FROM python:3.8

WORKDIR /appfolder

COPY . .
RUN pip install -r requirements.txt
CMD ["python3.8","main.py", "echo SECRET_KEY=YOUR_SECRET_KEY > .env", "uvicorn main:app --reload"]