from celery_run import app
from database.databasehandler import DatabaseHandler
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse


class Scraper:
    """
    Scraper defines API for creating and executing scraping tasks
    """
    def create_scraping_task(self, url, data_type, tag):
        """
        Create new scraping task and send it to the worker server
        :param url: url to scrap from
        :param data_type: data type to scrap from the website
        :param tag: optional tag to add to the scraped data
        :return: id of the new scraping task
        """
        scrape(url, data_type, tag)


@app.task(ignore_result=True)
def scrape(url, data_type, tag):
    """
    Create new scraping task and send it to the worker server
    """
    connector = DatabaseHandler(app.conf.result_backend.split('/')[-1])
    id = connector.create_task((url, tag, data_type, True))
    if data_type == 'images':
        (fetch_page.s(url) | parse_page.s(data_type) | download_images.s(tag) | mark_finished.si(id))()
    elif data_type == 'texts':
        (fetch_page.s(url) | parse_page.s(data_type) | store_text.s(url, tag) | mark_finished.si(id))()

@app.task(ingnore_result=True)
def fetch_page(url):
    """
    Fetches page
    """
    r = requests.get(url)
    return r.text

@app.task(ingnore_result=True)
def parse_page(page, data_type):
    """
    Parse page and return either text or list or images' urls
    """
    soup = BeautifulSoup(page, 'html.parser')
    if data_type == 'texts':
        return soup.get_text()
    elif data_type == 'images':
        return [img_tag.get('src') for img_tag in soup.find_all('img', {'src':re.compile('.(jpg|png|jpeg|bmp)')})]

@app.task(ingnore_result=True)
def download_images(url_list, tag):
    """
    Iterate over list of urls and if valid fetch it and save in the database
    :return:
    """
    for url in url_list:
        try:
            if urlparse(url).scheme and urlparse(url).netloc:
                response = requests.get(url)
                data = response.content
                if response.status_code == 200:
                    connector = DatabaseHandler(app.conf.result_backend.split('/')[-1])
                    connector.save_data(data=data, url=url, tag=tag, table='images')
        except Exception:
            # For now omit that url
            pass

@app.task(ingnore_result=True)
def store_text(data, url, tag):
    """
    Store scraped data
    :return:
    """
    connector = DatabaseHandler(app.conf.result_backend.split('/')[-1])
    connector.save_data(data=data, url=url, tag=tag, table='texts')

@app.task(ignore_result=True)
def mark_finished(id):
    connector = DatabaseHandler(app.conf.result_backend.split('/')[-1])
    connector.update_task(id, False)
