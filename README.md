# ikigai

[![dev](https://github.com/paulnicolet/ikigai/actions/workflows/dev.yaml/badge.svg)](https://github.com/paulnicolet/ikigai/actions/workflows/dev.yaml)
[![codecov](https://codecov.io/github/paulnicolet/ikigai/branch/main/graph/badge.svg?token=8VND8ZPWL9)](https://codecov.io/github/paulnicolet/ikigai)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Activities fetching strategy

We use the following strategy to cache Strava activities and avoid making API calls when client request a random activity.

❌ = not implemented
✅ = implemented
📅 = let as future work

1. ❌ **Upon account creation**:
   1. ❌ Download one activity in sync to ensure user is served right away.
   2. ✅ Download 5 activities async to ensure user have data if playing around a few seconds after login.
   3. ✅ Enqueue the rest in the job queue to ensure that ultimately we download all the backlog.
   4. ❌ Dequeue jobs async and periodically: 10 items every 15 minutes to comply with Strava rate limit (max 100 / 15 minutes, we let room for new incoming users).
2. ✅ **Upon new activity**: we are notified with the Strava webhook and enqueue a fetch job.
3. 📅 **Periodic backfilling**: could be useful to ensure consistency and not only rely on webhooks. Let as future work.

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
