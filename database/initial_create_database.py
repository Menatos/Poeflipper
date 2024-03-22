import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from database.db_provider import create_db_tables, refresh_db_values, refresh_old_league_prices

create_db_tables()
refresh_db_values()
refresh_old_league_prices()