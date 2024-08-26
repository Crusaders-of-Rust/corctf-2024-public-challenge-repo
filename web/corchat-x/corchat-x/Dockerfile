FROM --platform=amd64 python:3.12-alpine

WORKDIR /opt

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY static ./static
COPY templates ./templates
COPY app.py .

CMD ["python", "app.py"]