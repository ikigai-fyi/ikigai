# memories

## Setting up the environment for development

First setup the `.env` file

`touch .env`

`echo 'APP_CONFIG="local"' >> .env`

`echo 'FLASK_APP="app:create_app()"' >> .env`

`echo 'FLASK_DEBUG=1' >> .env`

`echo 'FLASK_ENV=development' >> .env`

Then, run

`pipenv sync --dev`

`pipenv shell`

## Running the server

`flask run`