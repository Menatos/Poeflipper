import time
import schedule
from database import db_provider

# Schedule the job to run every 60 minutes
schedule.every(60).minutes.do(db_provider.refresh_db_values)

while True:
    schedule.run_pending()
    time.sleep(1)
