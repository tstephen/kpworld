import os
from pathlib import Path
import subprocess
import sys

def generate():
    """Invoke fastapi-code-generator with the OpenAPI spec, generating separate routers."""
    result = subprocess.run(
        [
            sys.executable, "-m", "fastapi_code_generator",
            "--input", "api/openapi.yaml",
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

def init_db():
    """Initialize the database schema and add initial data."""
    print("Starting database if not running...")
    try:
        start_db()
    except subprocess.CalledProcessError:
        print("Database already running")

    print("Running database migrations...")
    subprocess.run([
        sys.executable, "-m", "alembic",
        "upgrade", "head"
    ], check=True)

    print("Adding initial data...")
    from kpworld.database import SessionLocal
    from kpworld.db_models import User, Article, Tag
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = SessionLocal()

    # Add demo user if it doesn't exist
    if not db.query(User).filter(User.email == "demo@demo.com").first():
        demo_user = User(
            email="demo@demo.com",
            username="demo",
            hashed_password=pwd_context.hash("demo"),
            bio="I'm a demo user",
            image="https://api.realworld.io/images/demo-avatar.png"
        )
        db.add(demo_user)
        db.commit()
        
        # Add some tags
        tags = [
            Tag(name="dragons"),
            Tag(name="training"),
            Tag(name="nodejs"),
            Tag(name="fastapi")
        ]
        db.add_all(tags)
        db.commit()

        # Add a demo article
        article = Article(
            title="Welcome to KP World",
            description="A Real World implementation in FastAPI",
            body="This is a demo article in the KP World implementation.",
            slug="welcome-to-kp-world",
            author_id=demo_user.id,
            tags=tags[:2]  # Add first two tags to article
        )
        db.add(article)
        db.commit()

    db.close()
    print("Database initialization complete!")