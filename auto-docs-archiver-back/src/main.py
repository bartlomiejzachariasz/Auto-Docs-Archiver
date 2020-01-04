from src.api.app import app
from src.resources.config import SERVER_CONFIG

if __name__ == "__main__":
    app.run(host=SERVER_CONFIG["host"], port=SERVER_CONFIG["port"])
