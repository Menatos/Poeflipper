import json
from datetime import datetime


def log_json(data, log_file="log.log"):
    timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")
    log_entry = {"timestamp": timestamp, "data": data}

    with open(log_file, "a") as file:
        file.write(json.dumps(log_entry) + "\n")
