FROM python:3.11-slim

WORKDIR /app

COPY ./app/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--reload","--port", "80"]