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