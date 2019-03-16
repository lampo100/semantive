from flask import Flask, g, request, jsonify, current_app, make_response
from config_example import FlaskConfig
from scraper.scraper import Scraper
from database.databasehandler import DatabaseHandler
import imghdr

app = Flask('semantive')
app.config.from_object(FlaskConfig)

def get_scraper():
    return g.setdefault('scraper', Scraper())

def get_connector():
    return g.setdefault('db_connector', DatabaseHandler(current_app.config['DATABASE']))

@app.route('/api/scraping-tasks/', methods=['GET'])
def get_scraping_tasks():
    """
    Returns collection of all the scraping tasks in the system
    :return: all scraping tasks
    """
    url = request.args.get('website-url')
    tasks =  get_connector().get_tasks_collection(url=url)
    return jsonify(tasks)

@app.route('/api/scraping-tasks/', methods=['POST'])
def create_scraping_task():
    """
    Create new scraping task and send it the task queue
    :return: OK if created
    """
    data = request.get_json()
    if not data:
        return 'Bad request', 400
    url = data.get('url')
    data_type = data.get('data_type')
    tag = data.get('tag')
    if None in (url, data_type, tag):
        return 'Bad request', 400
    get_scraper().create_scraping_task(url=url, data_type=data_type, tag=tag)
    return 'OK'

@app.route('/api/scraping-tasks/<string:uuid>', methods=['GET'])
def get_scraping_task_by_id(uuid):
    """
    Get information about scraping task with given uuid
    :param id: uuid of the task to return
    :return: information about given task
    """
    data = get_connector().get_task(uuid=uuid)
    if not data:
        return 'Task with given id does not exist', 404
    return jsonify(data)

@app.route('/api/images/', methods=['GET'])
def get_images():
    """
    Get collection of all images in the system
    :return: collection of all images
    """
    url = request.args.get('website-url')
    tag = request.args.get('tag')
    images =  get_connector().get_images_collection(url=url, tag=tag)
    return jsonify(images)

@app.route('/api/images/<int:id>/', methods=['GET'])
def get_image_by_id(id):
    """
    Return image resource with given id
    :param id: id of wanted image resource
    :return:
    """
    data = get_connector().get_image(id=id)
    if not data:
        return 'Image with given id does not exist', 404
    return jsonify(data)

@app.route('/api/images/<int:id>/', methods=['DELETE'])
def delete_image(id):
    """
    Delete image resource with given id
    :param id: id of image to delete
    :return:
    """
    data = get_connector().get_image(id=id)
    if not data:
        return 'Image with given id does not exist', 404
    get_connector().delete_image(id=id)
    return 'Image removed', 204

@app.route('/api/images/<int:id>/content', methods=['GET'])
def get_image_content(id):
    """
    Return content of an image with given id
    :param id: id of wanted image
    :return: image
    """
    data = get_connector().get_image_content(id=id)
    if not data:
        return 'Image with given id does not exist', 404
    response = make_response(data.get("content"), 200)
    response.headers['Content-Type'] = imghdr.what(None, h=data)
    return response

@app.route('/api/texts/', methods=['GET'])
def get_texts():
    """
    Get collection of all texts in the system
    :return: collection of all texts
    """
    url = request.args.get('website-url')
    tag = request.args.get('tag')
    texts =  get_connector().get_texts_collection(url=url, tag=tag)
    return jsonify(texts)

@app.route('/api/texts/<int:id>/', methods=['GET'])
def get_text_by_id(id):
    """
    Return text resource with given id
    :param id: id of wanted text resource
    """
    data = get_connector().get_text(id=id)
    if not data:
        return 'Text with given id does not exist', 404
    return jsonify(data)

@app.route('/api/texts/<int:id>/', methods=['DELETE'])
def delete_text(id):
    """
    Delete text resource with given id
    :param id: id of text to delete
    :return:
    """
    data = get_connector().get_text(id=id)
    if not data:
        return 'Text with given id does not exist', 404
    get_connector().delete_text(id=id)
    return 'Text removed', 204

@app.route('/api/texts/<int:id>/content', methods=['GET'])
def get_text_content(id):
    """
    Return content of a text with given id
    :param id: id of wanted text
    """
    data = get_connector().get_text_content(id=id)
    if not data:
        return 'Text with given id does not exist', 404
    response = make_response(data.get("content"), 200)
    response.headers['Content-Type'] = 'text/plain'
    return response


if __name__ == '__main__':
    app.run()