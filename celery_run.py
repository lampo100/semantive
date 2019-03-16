from celery import Celery
from config_example import CeleryConfif

app = Celery(__name__, config_source=CeleryConfif)