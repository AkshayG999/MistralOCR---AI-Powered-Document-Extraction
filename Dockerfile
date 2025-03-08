FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Use the run script to start both services
CMD ["python", "run_app.py"]
