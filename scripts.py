import subprocess 

def echo() -> None:
    """Start the Echo server."""
    subprocess.run(["fastapi", "dev", "nlip_server/echo.py"])
