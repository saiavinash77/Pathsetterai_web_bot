FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and frontend
COPY app/ /app/app/
COPY frontend/ /app/frontend/
COPY data/ /app/data/
COPY chroma_store/ /app/chroma_store/

# Set environment (override in deployment)
ENV GROQ_API_KEY=""

# Expose port
EXPOSE 8000

# Run production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
