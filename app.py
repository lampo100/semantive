from flask import Flask, request, jsonify, _app_ctx_stack
from flask_negotiate import consumes, produces
import sqlite3

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


DATABASE = './database.db'

def get_db():
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is None:
        db = _app_ctx_stack.top._database = sqlite3.connect(DATABASE)
    return db

@flask_app.teardown_appcontext
def close_connection(exception):
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is not None:
        db.close()


@flask_app.route('/api/scraping-tasks', methods=['GET'])
def get_scraping_tasks():
    """
    Returns collection of all the scraping tasks in the system
    :return: all scraping tasks
    """
    return 'Scraping tasks collection'

@flask_app.route('/api/scraping-tasks', methods=['POST'])
@consumes('application/json')
def create_scraping_task():
    data = request.get_json()

    print('Creating new task {}'.format(request.get_json()))
    return jsonify({"created": "blablabla", "link":"127.0.0.1:5000/api/scrapingfsda"})

@flask_app.route('/api/scraping-tasks', methods=['PUT'])
def update_scraping_tasks():
    return 'Scraping tasks collection'

@flask_app.route('/api/scraping-tasks/<int:id>', methods=['GET'])
def get_scraping_task(id):
    """
    Get information about scraping task with given id
    :param id: id of the task to return
    :return: information about given task
    """
    return "Wanted scraping task {}".format(id)

@flask_app.route('/api/images/', methods=['GET'])
def get_images():
    """
    Get collection of all images in the system
    :return: collection of all images
    """
    return "All images here:"

@flask_app.route('/api/images/<int:id>', methods=['GET'])
def get_image_by_id(id):
    """
    Return image resource with given id
    :param id: id of wanted image resource
    :return:
    """
    return "Here is image number {}".format(id)

@flask_app.route('/api/images/<int:id>', methods=['DELETE'])
def delete_image(id):
    """
    Delete image resource with given id
    :param id: id of image to delete
    :return:
    """
    return "Here is image number {}".format(id)

@flask_app.route('/api/images/<int:id>/content', methods=['GET'])
def get_image_content(id):
    """
    Return content of an image with given id
    :param id: id of wanted image
    :return: image
    """
    return "Here is content of an image with id {}".format(id)

@flask_app.route('/api/texts')
def get_texts():
    """
    Get collection of all texts in the system
    :return: texts collection
    """
    return "Here are all the texts in the system"

@flask_app.route('/api/texts/<int:id>')
def get_text_by_id(id):
    """
    Return wanted text with given id
    :param id: id of a wanted text
    :return: text
    """
    return "Here is your text with id {}".format(id)

@flask_app.route('/api/texts/<int:id>/content')
def get_text_content(id):
    """
    Get content of an image with given id
    :param id: id of wanted image
    :return: image
    """
    return "here is content of image with id {}".format(id)
