# Commands
pip install -r requirements-dev.txt --force

uvicorn main:app --env-file environment.txt --port 8000 --reload

normal:
pytest --cov-report term-missing --cov=gql_projects tests

strict:
pytest --cov-report term-missing --cov=gql_projects tests -x