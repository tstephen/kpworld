KP World
========

An implementation of [Real World](https://github.com/gothinkster/realworld) backend in Python using FastAPI.

Real World is a sample blogging application with contract between front and back ends defined by
<api/openapi.yaml>

## Run application and tests

1. Pre-requisites:
   - Python 3.12 installed
   - [Poetry 2.x installed](https://python-poetry.org/docs/#installation)
   - Docker installed (to run database)

1. Install dependencies

   ```sh
   poetry install
   ```

1. Start database and insert minimal test data.

   ```sh
   poetry run init-db
   ```

1. Start local application server

   ```sh
   poetry run server
   ```

1. Explore API endpoints at http://localhost:8000/api/docs

1. Run Real World tests to verify API compliance

   ```sh
   cd api && APIURL=http://localhost:8000/api ./run-api-tests.sh | tee -a results.log
   ```

1. If you want to connect to the database directly

   ```sh
    psql -h 127.0.0.1 -p 5432 -U kpworld kpworld
    ```