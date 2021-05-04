FROM debian:buster-slim
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "gunicorn" , "--workers=2",  "app:app"]
