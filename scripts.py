import os
from pathlib import Path
import subprocess
import sys

def generate():
    """Invoke fastapi-code-generator with the OpenAPI spec, generating separate routers."""
    result = subprocess.run(
        [
            sys.executable, "-m", "fastapi_code_generator",
            "--input", "docs/openapi.yaml",
            "--output", "kpworld",
            "--generate-routers"
        ],
        check=True
    )
    return result.returncode

def server():
    """Start the FastAPI server using uvicorn."""
    subprocess.run(
        [
            sys.executable, "-m", "uvicorn",
            "kpworld.main:app",
            "--reload"
        ],
        check=True
    )

def start_db():
    """Start a PostgreSQL Docker container for local development."""
    db_name = os.environ.get("POSTGRES_DB", "kpworld")
    db_user = os.environ.get("POSTGRES_USER", "kpworld")
    db_password = os.environ.get("POSTGRES_PASSWORD", "kpworld")
    db_port = os.environ.get("POSTGRES_PORT", "5432")
    container_name = os.environ.get("POSTGRES_CONTAINER", "kpworld-postgres")

    subprocess.run([
        "docker", "run", "--rm", "-d",
        "--name", container_name,
        "-e", f"POSTGRES_DB={db_name}",
        "-e", f"POSTGRES_USER={db_user}",
        "-e", f"POSTGRES_PASSWORD={db_password}",
        "-p", f"{db_port}:5432",
        "postgres:16"
    ], check=True)

    # Optionally, create a .env file for SQLAlchemy connection string
    env_path = Path(".env")
    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:{db_port}/{db_name}"
    env_content = f"DATABASE_URL={db_url}\n"
    if not env_path.exists():
        env_path.write_text(env_content)
    else:
        lines = env_path.read_text().splitlines()
        if not any(line.startswith("DATABASE_URL=") for line in lines):
            env_path.write_text(env_content + "\n" + "\n".join(lines))

def stop_db():
    """Stop and remove the PostgreSQL Docker container used for local development."""
    container_name = os.environ.get("POSTGRES_CONTAINER", "kpworld-postgres")
    subprocess.run(
        ["docker", "stop", container_name],
        check=False
    )