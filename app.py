from flask import Flask, Response

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

@app.route('/api/scraping-tasks/', methods=['GET'])
def get_scraping_tasks():
    """
    Returns collection of all the scraping tasks in the system
    :return: all scraping tasks
    """
    return 'Scraping tasks collection'

@app.route('/api/scraping-tasks/', methods=['POST'])
def create_scraping_task():
    """
    Create new scraping task and send it the task queue
    :return: OK if created
    """
    return ('', 201)

@app.route('/api/scraping-tasks/', methods=['PUT'])
def update_scraping_tasks():
    """
    Updates statuses of given tasks
    :return: OK if processed
    """
    return 'OK'

@app.route('/api/scraping-tasks/<int:id>/', methods=['GET'])
def get_scraping_task_by_id(id):
    """
    Get information about scraping task with given id
    :param id: id of the task to return
    :return: information about given task
    """
    return "Wanted scraping task {}".format(id)

@app.route('/api/scraping-tasks/<int:id>/', methods=['DELETE'])
def delete_scraping_task(id):
    """
    Stop and delete scraping task
    :param id: id of the task to delete
    """
    return ("Deleted scraping task {}".format(id), 204)

@app.route('/api/scraping-tasks/<int:id>/', methods=['PUT'])
def update_scraping_task(id):
    """
    Update scraping task
    :param id: id of the task to delete
    """
    return ("Updated scraping task {}".format(id), 204)

@app.route('/api/images/', methods=['GET'])
def get_images():
    """
    Get collection of all images in the system
    :return: collection of all images
    """
    return "All images here:"

@app.route('/api/images/<int:id>/', methods=['GET'])
def get_image_by_id(id):
    """
    Return image resource with given id
    :param id: id of wanted image resource
    :return:
    """
    return "Here is image number {}".format(id)

@app.route('/api/images/<int:id>/', methods=['DELETE'])
def delete_image(id):
    """
    Delete image resource with given id
    :param id: id of image to delete
    :return:
    """
    return ("Here is image number {}".format(id), 204)

@app.route('/api/images/<int:id>/content', methods=['GET'])
def get_image_content(id):
    """
    Return content of an image with given id
    :param id: id of wanted image
    :return: image
    """
    return "Here is content of an image with id {}".format(id)

@app.route('/api/texts/', methods=['GET'])
def get_texts():
    """
    Get collection of all texts in the system
    :return: collection of all texts
    """
    return "All texts"

@app.route('/api/texts/<int:id>/', methods=['GET'])
def get_text_by_id(id):
    """
    Return text resource with given id
    :param id: id of wanted text resource
    """
    return "Here is text number {}".format(id)

@app.route('/api/texts/<int:id>/', methods=['DELETE'])
def delete_text(id):
    """
    Delete text resource with given id
    :param id: id of text to delete
    :return:
    """
    return ("Deleted text number {}".format(id), 204)

@app.route('/api/texts/<int:id>/content', methods=['GET'])
def get_text_content(id):
    """
    Return content of a text with given id
    :param id: id of wanted text
    """
    return "Here is content of a text with id {}".format(id)