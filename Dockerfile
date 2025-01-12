# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2 \
    libcairo2-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    fonts-liberation \
    libharfbuzz-icu0 \
    default-libmysqlclient-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file separately for caching
COPY requirements.txt .

# Install Python dependencies (cache-friendly)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Define the command to run the application
CMD ["python","run.py"]
