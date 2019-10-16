
import threading
import logging

from flask_api import FlaskAPI

from .api_v1 import api as api_v1

SERVICE_NAME = "api_service"

app = FlaskAPI(__name__)


class ApiService(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self._stop_event = threading.Event()


    def stop(self):
        self._stop_event.set()


    def run(self):
        while True:
            app.register_blueprint(api_v1)
            thread = threading.Thread(name=SERVICE_NAME, target=app.run, kwargs=dict(threaded=True))
            thread.start()
            logging.info(f"Start {SERVICE_NAME}.")

            thread.join()

            if self._stop_event.is_set():
                break

            logging.warning(f"Down {SERVICE_NAME}.")

        return
