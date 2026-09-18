import logging
import sys
from threading import Thread

from flask import Flask, request

HOST = "0.0.0.0"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s (%(threadName)s): %(message)s"

app = Flask("Server")


def _configure_logging() -> None:
    """Send records below ERROR to stdout and ERROR and above to stderr.

    The EEC captures both streams separately, so splitting them keeps genuine
    failures out of the informational log.
    """
    formatter = logging.Formatter(LOG_FORMAT)

    error_handler = logging.StreamHandler()
    error_handler.addFilter(lambda record: record.levelno >= logging.ERROR)
    error_handler.setFormatter(formatter)

    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    std_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT,
                        handlers=[error_handler, std_handler])
    logging.raiseExceptions = False


_configure_logging()


@app.route("/upload", methods=["POST"])
def upload():
    """Accept a JSON payload and log it."""
    payload = request.get_json(silent=True)
    if payload is None:
        app.logger.warning("POST /upload rejected: body is not valid JSON")
        return {"message": "Request body must be valid JSON"}, 400

    app.logger.info("POST /upload received payload: %s", payload)
    return {"message": "Payload received"}


@app.route("/info", methods=["GET"])
def info():
    """Liveness probe."""
    app.logger.info("GET /info")
    return {"message": "info"}


class Server(Thread):
    """Runs the Flask app on `port`, listening on all addresses.

    Started as a daemon thread so it does not block extension shutdown.
    """

    def __init__(self, port: int):
        super().__init__(daemon=True, name="Server")
        self.port = port

    def run(self):
        app.run(host=HOST, port=self.port, debug=False, use_reloader=False)
