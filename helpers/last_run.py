import datetime
import os
from os.path import join, dirname

from dotenv import load_dotenv

env_path = join(os.path.abspath(os.path.join(os.getcwd())), ".env")
load_dotenv(env_path)

fmt = "%d.%m.%y %H:%M:%S"

if os.environ.get("ENVIRONMENT") == "production":
    log_path = "logs/last_run.log"
else:
    log_path = "../logs/last_run.log"

def get_last_run_time_stamp():
    # Try loading the datetime of the last run from the log file
    try:
        with open(log_path, mode="r") as file:
            lines = file.readlines()
            if lines:
                return datetime.datetime.strptime(str(lines[-1].rsplit(" ", 1)[0]).strip(), fmt)
            else:
                return datetime.datetime.now().strftime(fmt)
    except FileNotFoundError:
        # Return with current time-stamp if last_run.log file is not present
        return datetime.datetime.now().strftime(fmt)


def save_last_run_time_stamp(prefix='unknown'):
    filename = log_path

    if not os.path.exists(filename):
        open(filename, "w+").close()
    # Update the script execution time and save it to the log file
    with open(filename, mode="a") as file:  # Use "a" for append mode
        current_timestamp = datetime.datetime.now().strftime(fmt) + " " + prefix
        file.write(current_timestamp + "\n")  # Write current timestamp to a new line