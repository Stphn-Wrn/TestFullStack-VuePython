# TestFullStack-VuePython

I'm aware that some things haven't been implemented in full, or perhaps only in part, or that others need to be improved. 

I was able to discover Vue3 and its API composition, which I'd never used before, or JWT directly via cookies with interceptors. It was all very interesting. 
As for Python, I'd already used it for a few scripts in my personal projects, but never really for the web. It was fun to use and I enjoyed it. 

As for the tests, I didn't have the time to do them all for all the features, but if I'd had the time, I'd have set up a complete e2e, I think. It's a test I didn't know about and the principle is great.


The project requires [poetry](https://python-poetry.org/docs/):

```shell
$ pip install -U pip setuptools
$ pip install poetry
$ poetry install # run this if poetry is already installed
```

You can run docker compose through  :
```shell
$ docker compose --env-file ./backend/environment/.compose.env up  --build -d
OR
chmod +x start_dev.sh
THEN
sh start_dev.sh
```
Note: This docker configuration is stuffed with a Hot Reload Module system, you shouldn't need to relaunch at each change.

### Don't forget to create the .compose.env file in the alembic environment folder and the .env file in the project root. 

# Alembic (migration)

We use alembic to generate database auto migration

when you edit a model you can simply use this command to automatically generate a migration script:

```shell
$ poetry run alembic revision --autogenerate -m "the purpose of the migration briefly"
$ poetry run alembic upgrade head # apply the migration
```

# Start frontend 
```
/TestFullStack-VuePython/frontend
$ npm run dev
http://localhost:3000/
```

# Testing
```
/TestFullStack-VuePython : 
$ pytest backend/tests/unit
```
```
/frontend : 
$ cypress headless : npx cypress run --spec "frontend/cypress/e2e/file_to_test.cy.js"
$ cypress GUI with Electron : npx cypress open - E2E Testing - Start E2E Testing in Electron - chose script to test
```

# Linter :
```
/frontend
$ eslint --fix ./src
```



