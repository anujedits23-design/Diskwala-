# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Upgrade pip (important)
RUN pip install --upgrade pip

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for Flask)
EXPOSE 5000

# Run web server
CMD ["gunicorn", "web:app", "--bind", "0.0.0.0:5000"]
