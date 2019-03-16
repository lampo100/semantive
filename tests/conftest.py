import pytest
import os
from app import app
import tempfile
from database.databasehandler import DatabaseHandler

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()
    DatabaseHandler(app.config['DATABASE']).initialize_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])