import time
import schedule
from database import db_provider
import subprocess

# Schedule the job to run every 60 minutes
schedule.every(60).minutes.do(db_provider.refresh_db_values)
schedule.every(2).minutes.do(subprocess.run(["sudo", "git", "pull"], check=True, stdout=subprocess.PIPE).stdout)

while True:
    schedule.run_pending()
    time.sleep(1)
