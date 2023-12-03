ARG PYTHON_VERSION=3.11.5
FROM --platform=linux/x86_64 python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .


RUN apt-get update && \
    apt-get install -y libpq-dev gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install -r requirements.txt --no-cache-dir

EXPOSE 3000
CMD python -m src.main
