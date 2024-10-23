import os
import subprocess
import sys

_SERVER_MODULE_PATH = "app.server:app"
_CHAT_SERVER_MODULE_PATH = "solutions.chat.chatbot:app"
_INTEGRATION_SERVER_MODULE_PATH = "solutions.integrator.integrator:app"


def format_code() -> None:
    """Format the code using black and isort."""
    for formatter in ("black", "isort"):
        print(f"Running {formatter}...")
        subprocess.run([formatter, "."], check=True)


def start_server() -> None:
    """Start the FastAPI server."""
    subprocess.run(
        ["uvicorn", _SERVER_MODULE_PATH, *compose_shared_flags()],
        check=True,
    )


def start_server_dev() -> None:
    """Start the FastAPI server in development mode."""
    subprocess.run(
        ["uvicorn", _SERVER_MODULE_PATH, *compose_shared_flags(), "--reload"],
        check=True,
    )


def start_chat_server() -> None:
    """Start the FastAPI chat server."""
    subprocess.run(
        ["uvicorn", _CHAT_SERVER_MODULE_PATH, *compose_shared_flags()],
        check=True,
    )


def start_integration_server() -> None:
    """Start the FastAPI integration server."""
    subprocess.run(
        [
            "uvicorn",
            _INTEGRATION_SERVER_MODULE_PATH,
            *compose_shared_flags(),
            "--reload",
        ],
        check=True,
    )


def compose_shared_flags() -> list[str]:
    """Compose shared command-line flags for Uvicorn."""
    return ["--host", "0.0.0.0", "--port", os.environ.get("PORT", "8006")]
