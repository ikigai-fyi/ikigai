# ikigai

[![dev](https://github.com/paulnicolet/ikigai/actions/workflows/dev.yaml/badge.svg)](https://github.com/paulnicolet/ikigai/actions/workflows/dev.yaml)
[![codecov](https://codecov.io/github/paulnicolet/ikigai/branch/main/graph/badge.svg?token=8VND8ZPWL9)](https://codecov.io/github/paulnicolet/ikigai)

## Setting up the environment for development

### Create the .env file

```
cp .env.examples .env
```

### Run a Postgres instance

The recommended way is using Docker:

```
$ docker pull postgres:13
$ docker run \
    --name postgres \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=admin \
    -e POSTGRES_DB=ikigai \
    -p 5432:5432 \
    -d postgres:13
```

Make sure to adjust the database URL in your .env:

```
SQLALCHEMY_DATABASE_URI="postgresql+psycopg://admin:admin@localhost:5432/ikigai"
```

### Enable the virtual environment

```
rye sync && rye shell
```

### Running the server

```
flask run
```
