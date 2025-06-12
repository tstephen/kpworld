# Best practices for FastAPI RealWorld implementation

## Techology stack

- **Swagger/OpenAPI**: API documentation in `docs/openapi.yaml`.
- **FastAPI**: REST API implementation.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Database for storing data.
- **Alembic**: Database migrations.
- **Pydantic**: Data validation and serialization.
- **Poetry**: Dependency management and packaging.
- **pytest**: Testing framework.
- **Docker**: Containerization for development and deployment.
- **GitHub Actions**: CI/CD for automated testing and deployment.
- **Pre-commit hooks**: Code quality checks before commits.
- **Black**: Code formatting.
- **isort**: Import sorting.
- **mypy**: Static type checking.
- **bandit**: Security checks.
- **flake8**: Code style checks.
- **coverage.py**: Code coverage analysis.
- **httpx**: HTTP client for testing.
- **uvicorn**: ASGI server for running FastAPI applications.
- **pytest-asyncio**: Async testing support for pytest.
- **pytest-cov**: Plugin for pytest to measure code coverage.

## Project structure

```
kpworld
├── docs
│   └── openapi.yaml
├── kpworld
│   ├── dependencies.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── routers
│       ├── articles.py
│       ├── comments.py
│       ├── favorites.py
│       ├── profile.py
│       ├── tags.py
│       └── user_and_authentication.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── scripts.py
└── tests
    └── __init__.py
```

