import logging
import json
from datetime import datetime
import pytz  

class JSONFormatter(logging.Formatter):
    def format(self, record):
        tz = pytz.timezone('America/Argentina/Buenos_Aires')
        
        dt = datetime.fromtimestamp(record.created, tz)
        timestamp = dt.strftime(" %H:%M:%S %d-%m-%Y")
        
        log_record = {
            "timestamp": timestamp,
            "level": record.levelname,
            "event": record.msg
        }

        optional_fields = ["user_id", "review_id", "media_id"]
        for field in optional_fields:
            value = getattr(record, field, None)
            if value is not None:
                log_record[field] = value

        return json.dumps(log_record)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/logs/api-logs.log")
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)