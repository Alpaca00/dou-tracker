FROM python:3.12-slim

WORKDIR /app

COPY ../.. /app

RUN /usr/local/bin/python -m pip install --upgrade pip \
 && pip install -r /app/requirements.txt

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
CMD [""]