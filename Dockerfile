FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

ENV ALPHA_VANTAGE_API_KEY=your_api_key_here

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

EXPOSE 5000

ENV FLASK_APP=run.py

ENV FLASK_ENV=production

RUN mkdir -p /usr/src/app/database

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
