import datetime
import os
from os.path import join

from dotenv import load_dotenv

env_path = join(os.path.abspath(os.path.join(os.getcwd())), ".env")
load_dotenv(env_path)

fmt = "%d.%m.%y %H:%M:%S"

if os.environ.get("ENVIRONMENT") == "production":
    log_path = "logs/last_run.log"
else:
    log_path = "../logs/last_run.log"


def get_last_run_time_stamp():
    last_refresh_time = None

    try:
        with open(log_path, mode="r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                if "refresh_db_values" in line:
                    date_string = " ".join(line.split()[:2])  # Extract date and time parts
                    last_refresh_time = datetime.datetime.strptime(date_string, "%d.%m.%y %H:%M:%S")
                    break

        if last_refresh_time is None:
            return datetime.datetime.now().strftime(fmt)
        else:
            return last_refresh_time.strftime(fmt)

    except FileNotFoundError:
        return datetime.datetime.now().strftime(fmt)


def save_last_run_time_stamp(prefix='unknown'):
    filename = log_path

    if not os.path.exists(filename):
        open(filename, "w+").close()
    # Update the script execution time and save it to the log file
    with open(filename, mode="a") as file:  # Use "a" for append mode
        current_timestamp = datetime.datetime.now().strftime(fmt) + " " + prefix
        file.write(current_timestamp + "\n")  # Write current timestamp to a new line