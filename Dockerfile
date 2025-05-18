FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY company_list.txt .
COPY .env .

CMD ["python", "main.py"]

