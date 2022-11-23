python -m venv venv
venv/bin/active ^
& pip install -r requirements.txt & echo SECRET_KEY=YOUR_SECRET_KEY > .env & uvicorn main:app --reload