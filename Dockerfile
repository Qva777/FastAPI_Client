FROM python

WORKDIR /app

COPY . /Docker_app
RUN pip install -r requirements.txt
CMD ["python3.8","main.py"]