FROM python:3.9.16

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /app ./

ENTRYPOINT python ./app.py
# ENTRYPOINT bash
