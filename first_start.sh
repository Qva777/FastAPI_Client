python3 -m venv venv
source venv/bin/activate ^
& pip install -r requirements.txt ^
& echo SECRET_KEY=YOUR_SECRET_KEY > .env & uvicorn main:app --reload
