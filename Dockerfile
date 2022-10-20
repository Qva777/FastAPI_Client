FROM python

WORKDIR /app

COPY . .

CMD ["python3.8","main.py"]