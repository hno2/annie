# Annie

Annie is a framework for grading Jupyter Notebook Assignments. It models the whole process, from the distribution of notebooks to the manual grading and feedback. It offers an extensible and maintainable architecture for individualization

## Installation
The installation via docker-compose is highly recommended due to security concerns of running student code. 

### Docker 
The easiest way to get started is to use a reverse proxy (like [traefik](https://traefik.io/traefik/)) with docker-compose. You can find an example [docker-compose.yaml](docker-compose.yaml) in this repo. The sample docker-compose should spawn the required containers for the webapp, redis, and a celery worker, but will require you to set up the reverse proxy yourself. 
If necessary use the [Dockerfile](Dockerfile) provided to build your personalized image or use the [docker image](ghcr.io/hno2/annie:latest) build by the [GitHub Action](.github/workflows/main.yml).



### Manual (for Development)
1. Install the required packages (`pip install -r requirement.txt && pip install --no-deps -r no-deps.txt && pip install -r optimal.txt`)
2. Initialize the Database with `flask db reset` (checkout the [`db/seedy.py`](db/seeds.py) for the initial mock values)
3. Run the App `export FLASK_APP="annie.app:create_app()" && flask run`, point your browser to `localhost:5000` to see the results.

## Architecture
The functionality is split into multiple flask blueprints (`annie/blueprints`), each providing own view functions, templates and for  which are 
Core Templates, which are reused 

Functionality is kept as modular as possible by relying on flask Blueprints and factory methods. Configuration is done via the main configuration file 


Database Seeds can customized in the [seedy.py](db/seeds.py). 