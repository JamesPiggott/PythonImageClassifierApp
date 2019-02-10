FROM python:3.6-alpine

RUN apk add make automake gcc g++ subversion python3-dev

COPY requirements.txt /

# Install required dependencies
RUN pip install -r /requirements.txt

COPY src/ /app

WORKDIR /app

CMD ["gunicorn", "-w 4", "main:app"]
