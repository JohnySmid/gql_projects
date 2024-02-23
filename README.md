```bash
pip install -r requirements-dev.txt --force
```

```bash
uvicorn main:app --env-file environment.txt --port 8000 --reload
```

normal:
```bash
pytest --cov-report term-missing --cov=gql_projects tests
```

strict:
```bash
pytest --cov-report term-missing --cov=gql_projects tests -x
```