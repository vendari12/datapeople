FROM python:3.11-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc musl-dev && apt clean

RUN apt clean

WORKDIR /app

ENV PYTHONIOENCODING=UTF-8

COPY . /app/
COPY ./Procfile /app/


RUN python -m pip install --upgrade setuptools


RUN pip install --no-cache -r ./requirements.txt 

# Create a new user and switch to that user
RUN addgroup --system  datapeople  && \
    adduser --system jobboard --gid 101  && \
    chown -R jobboard:datapeople /app

 USER jobboard
# Expose the app port
EXPOSE 8000

CMD [ "gunicorn", "-c", "./server/gunicorn.conf.py", "manage:app" ]