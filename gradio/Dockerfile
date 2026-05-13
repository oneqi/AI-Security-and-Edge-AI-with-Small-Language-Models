# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables to optimize Python execution
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies if required for packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition file first to leverage Docker cache
COPY requirements.txt .

# Install Python application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
#COPY . .
COPY app.py /app/app.py

# Expose port if your app runs a server (e.g., FastAPI, Flask)
EXPOSE 7860

# environment variables 
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Define entrypoint command to run application
CMD ["python", "app.py"]