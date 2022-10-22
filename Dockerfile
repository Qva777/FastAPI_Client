FROM python:3.8

WORKDIR /appfolder

COPY . .
RUN pip install -r requirements.txt
CMD ["python","main.py", "uvicorn main:app --reload"]