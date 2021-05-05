FROM debian:buster-slim
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--workers=2","-b","0.0.0.0:8000", "app:app"]