FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python create_db.py

EXPOSE 80 81

CMD ["python", "nutrition_api.py"] 