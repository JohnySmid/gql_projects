###############################################################
#
# Zero phase
#
###############################################################
# Initialization of python
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.13-slim as prepare

# Install curl to enable standard health check
RUN apt update && apt install curl -y && rm -rf /var/cache/apk/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

###############################################################
#
# First phase
#
###############################################################
# Initialization of node

FROM node:16 as appdev
WORKDIR /app
COPY . .
RUN npm install -g dociql
RUN dociql fetch-schema --file ./IntrospectionQuery.txt

###############################################################
#
# Last phase
#
###############################################################
FROM prepare as executepython

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app/js
COPY --from=appdev /app/js /app/js

WORKDIR /app

COPY . /app

FROM prepare as tester
# Create /app directory
WORKDIR /app

# Copy Python files
COPY . /app

RUN python -m pip install -r requirements-dev.txt
RUN python -m pip install coverage pytest pytest-cov
RUN python -m pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils --log-cli-level=INFO

FROM prepare as runner
# Create /app directory
WORKDIR /app

# Copy Python files
COPY . /app

# ERROR
# Copy the fetched file from the fetchschema stage
# COPY --from=fetchschema /usr/src/IntrospectionQuery.txt /app/fetched-file.txt

# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--reload=True", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-t", "60", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
