FROM python:3.9-slim-buster as app
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

WORKDIR /app
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD ./no-deps.txt ./no-deps.txt
RUN pip install --no-deps -r no-deps.txt 
ENV FLASK_ENV="production" \
    FLASK_APP="annie.app"
COPY . /app
RUN flask db reset 

EXPOSE 8000
LABEL org.opencontainers.image.source https://github.com/hno2/annie
CMD [ "gunicorn", "--workers=2","-b","0.0.0.0:8000", "annie.app:create_app()"]
