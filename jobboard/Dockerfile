FROM pypy:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc musl-dev && apt clean

RUN apt clean

WORKDIR /app

ENV PYTHONIOENCODING=UTF-8

COPY . /app/


RUN python -m pip install --upgrade setuptools


RUN pip install --no-cache -r ./server/requirements.txt --extra-index-url https://$PYPI_USER:$PYPI_PASS@$PYPI_URL --trusted-host $PYPI_URL

# Create a new user and switch to that user
RUN addgroup --system  datapeople  && \
    adduser --system jobboard --gid 101  && \
    chown -R jobboard:datapeople /app

 USER jobboard
# Expose the app port
EXPOSE 8000

CMD [ "gunicorn", "-c", "./server/gunicorn.conf.py", "manage:app" ]