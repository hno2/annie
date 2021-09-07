FROM python:3.9-slim-buster
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT
COPY . /app
WORKDIR /app
ENV FLASK_ENV="production" \
    FLASK_APP="annie.app"
RUN pip install -r requirements.txt
RUN pip install --no-deps -r no-deps.txt 
RUN flask db reset 

EXPOSE 8000
LABEL org.opencontainers.image.source https://github.com/hno2/annie
ENTRYPOINT [ "gunicorn", "--workers=2","-b","0.0.0.0:8000", "annie.app:create_app()"]
