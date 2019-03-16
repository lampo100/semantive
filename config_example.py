class FlaskConfig:
    DEBUG=True
    ENV='development'
    SERVER_NAME="127.0.0.1:8000"
    DATABASE='./database.db'

class CeleryConfif:
    broker_url = 'redis://redis:6379/0'
    result_backend = 'db+sqlite:///database.db'
    task_serializer = 'json'
    worker_disable_rate_limits = True
    accept_content = ['json',]
    include=['scraper.scraper']
    broker_heartbeat=0

class DatabaseConfig:
    url = './database.db'