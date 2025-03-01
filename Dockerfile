###############################################################
#
# Zero phase
#
###############################################################

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.13-slim as pythonbase

# Installation of curl for standard health check
RUN apt update && apt install curl -y && rm -rf /var/cache/apk/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN echo "Installation of pip requirements"

# Install npm and dociql inside /app
RUN apt update && apt install -y npm
RUN npm install -g dociql@latest

RUN echo "Installation of npm & dociql inside /app"

# ###############################################################
# #
# # First phase
# #
# ###############################################################

# FROM node:16 as buildnode

# # Create app directory
# WORKDIR /usr/src

# # Create a minimal package.json for Docker build
# RUN echo '{}' > package.json

# # Copy your project's package*.json files
# COPY package*.json ./
# RUN npm install

# ###############################################################
# #
# # Second phase
# #
# ###############################################################
# FROM buildnode as generate-docs

# # Create a directory for storing the documentation
# WORKDIR /usr/src/docs

# # Copy necessary files for dociql documentation generation
# COPY IntrospectionQuery.txt /usr/src/docs/
# COPY GraphQLSchema.graphql /usr/src/docs/
# COPY config.yml /usr/src/docs/
# # Update dociql to the latest version
# RUN npm install -g dociql

# # Run dociql to generate documentation inside /usr/src/docs
# #RUN dociql -a IntrospectionQuery.txt
# #RUN dociql -c config.yml
# #RUN dociql -d config.yml
# RUN dociql -d GraphQLSchema.graphql config.yml -t /usr/src/docs/
# #RUN dociql -d config.yml -t /usr/src/docs/
# RUN echo "Generated dociql documentation"

###############################################################
#
# Last phase
#
###############################################################

FROM pythonbase as prepare

EXPOSE 8000 4400

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# npm copy
# WORKDIR /app/dociql

# python copy
WORKDIR /app
COPY . /app


FROM prepare as tester
RUN python -m pip install -r requirements-dev.txt
RUN python -m pip install coverage pytest pytest-cov
RUN python -m pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils --log-cli-level=INFO


FROM prepare as runner
# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden.
# For more information, please refer to https://aka.ms/vscode-docker-python-debug 
#CMD ["bash", "-c", "gunicorn --bind 0.0.0.0:8000 -t 60 -k uvicorn.workers.UvicornWorker main:app"]
CMD ["bash", "-c", "gunicorn --bind 0.0.0.0:8000 -t 60 -k uvicorn.workers.UvicornWorker main:app & dociql -p 4400 -d config.yml"]