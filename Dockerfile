FROM python:slim

ENV FLASK_APP=main.py
COPY requirements.txt requirements.txt
COPY src .
RUN pip3 install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app --preload
