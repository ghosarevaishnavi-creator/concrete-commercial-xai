FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Streamlit default and API port
EXPOSE 8501 8000

# Default API key for demo; set a real one in production
ENV API_KEY=CHANGE_ME

# Start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
