import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "event": record.msg,
            "user_id": getattr(record, "user_id", None)
        }
        return json.dumps(log_record)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/logs/myapp.log")
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)