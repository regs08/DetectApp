import logging
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record, self.datefmt)

        log_entry = {
            "timestamp": record.asctime,
            "level": record.levelname,
            "message": record.msg,
            # Add any other fields as required
        }
        return json.dumps(log_entry)


