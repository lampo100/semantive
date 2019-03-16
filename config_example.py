class FlaskConfig:
    DEBUG=True
    ENV='development'
    SERVER_NAME="127.0.0.1:5000"
    TEST_VALUE=44
    DATABASE='./database.db'

class CeleryConfif:
    broker_url = 'amqp://localhost'
    result_backend = 'db+sqlite:///database.db'
    task_serializer = 'json'
    worker_disable_rate_limits = True
    accept_content = ['json',]
    include=['scraper.scraper']
    broker_heartbeat=0

class DatabaseConfig:
    url = './database.db'