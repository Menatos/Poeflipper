import time
import schedule
import db_provider

# Schedule the job to run every 2 minutes
schedule.every(30).minutes.do(db_provider.refresh_db_values)

while True:
    schedule.run_pending()
    time.sleep(1)
