FROM python:3.9-slim-buster
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -r --no-deps no-deps.txt 

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--workers=2","-b","0.0.0.0:8000", "app:app"]
