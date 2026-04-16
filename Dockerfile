FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Entrena el modelo dentro del build → pkl compatible con este Python/NumPy
RUN python model/train_model.py

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:server"]