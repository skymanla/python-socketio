FROM python:3.9-slim

WORKDIR /data

COPY requirements.txt /app/

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "app2.py", "--host=0.0.0.0"]