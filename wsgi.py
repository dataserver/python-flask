import logging
import time
from pathlib import Path

from flaskapp import create_app

BASE_PATH = Path(__file__).parent
log_date = time.strftime("%Y-%m-%d", time.localtime())
log_file = str(Path(BASE_PATH, "logs", f"log-{log_date}.log"))
logging.basicConfig(
    filename=log_file,
    format="[%(asctime)s] %(levelname)s | %(module)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.CRITICAL,
)

app = create_app(config_name="production")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
