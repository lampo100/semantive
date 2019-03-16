from database.databasehandler import DatabaseHandler
from config_example import DatabaseConfig

if __name__ == '__main__':
    DatabaseHandler(DatabaseConfig.url).initialize_db()