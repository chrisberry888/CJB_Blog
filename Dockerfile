FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

COPY . .

RUN chmod +x /app/docker/entrypoint.sh \
    && mkdir -p /app/data /app/media /app/staticfiles

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "personal_site.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

