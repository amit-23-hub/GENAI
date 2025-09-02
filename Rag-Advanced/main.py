
import uvicorn
from .server import app


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


main() # run the server when main.py is executed directly

