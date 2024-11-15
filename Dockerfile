FROM python:3.10-slim

# Update and install system dependencies step-by-step
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common && \
    apt-get install -y --no-install-recommends libgirepository1.0-dev || echo "libgirepository1.0-dev failed" && \
    apt-get install -y --no-install-recommends libcairo2 || echo "libcairo2 failed" && \
    apt-get install -y --no-install-recommends libgobject-2.0-0 || echo "libgobject-2.0-0 failed" && \
    apt-get install -y --no-install-recommends libpango-1.0-0 || echo "libpango-1.0-0 failed" && \
    apt-get install -y --no-install-recommends fonts-liberation || echo "fonts-liberation failed" && \
    apt-get install -y --no-install-recommends libharfbuzz-icu0 || echo "libharfbuzz-icu0 failed" && \
    apt-get install -y --no-install-recommends libpangoft2-1.0-0 || echo "libpangoft2-1.0-0 failed" && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENV SQLALCHEMY_DATABASE_URI=sqlite:///app.db

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
