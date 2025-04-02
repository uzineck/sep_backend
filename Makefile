DC = docker compose

# Docker-compose file paths
STORAGES_FILE = news_docker_compose/storages.yaml
APP_FILE = news_docker_compose/app.yaml

# Docker-compose container names
APP_CONTAINER = news_app
DB_CONTAINER = news_db

# Docker commands
EXEC = docker exec
EXEC_IT = docker exec -it
LOGS = docker logs

# Env file path(with docker argument)
ENV = --env-file .env

# Django application specific command
MANAGE_PY = python manage.py

.PHONY: all,
.PHONY: app, app-down, app-logs, # start,end,logs of the main app
.PHONY: storages, storages-logs, storages-down,  # storages(postgres, pgadmin, redis, redisinsight) commands
.PHONY: postgres, db-logs, # postgres specific commands
.PHONY: migrations, migrate, superuser, collectstatic # django manage.py commands

app:
		${DC} ${ENV} -f ${APP_FILE} -f ${STORAGES_FILE} up --build -d

app-logs:
		${LOGS} ${APP_CONTAINER} -f

app-down:
		${DC} ${ENV} -f ${APP_FILE} -f ${STORAGES_FILE} down

storages:
		${DC} ${ENV} -f ${STORAGES_FILE} up -d

storages-down:
		${DC} -f ${STORAGES_FILE} down

storages-logs:
		${DC} -f ${STORAGES_FILE} logs -f

db-logs:
		${LOGS} ${DB_CONTAINER} -f

postgres:
		@DB_USER=${DB_USER} DB_NAME=${DB_NAME} ${EXEC_IT} ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME}

migrate:
		${EXEC_IT} ${APP_CONTAINER} ${MANAGE_PY} migrate

migrations:
		${EXEC_IT} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

superuser:
		${EXEC_IT} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser --no-input

collectstatic:
		${EXEC_IT} ${APP_CONTAINER} ${MANAGE_PY} collectstatic
