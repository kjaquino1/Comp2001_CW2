FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libodbc1 \
    gcc \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
