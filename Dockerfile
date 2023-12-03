# PROD
#
# ARG PYTHON_VERSION=3.11.5
# FROM --platform=linux/x86_64 python:${PYTHON_VERSION}-slim as base
#
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
#
# WORKDIR /app
# COPY . .
#
#
# RUN apt-get update && \
#     apt-get install -y libpq-dev gcc build-essential && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/* && \
#     python -m pip install -r requirements.txt --no-cache-dir
#
# EXPOSE 3000
# CMD python -m src.main
#
# DEV

ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .
EXPOSE 3000
CMD python -m src.main
