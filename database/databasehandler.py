import sqlite3
import uuid

class DatabaseHandler:
    """
    Implements methods for interacting with database holding texts and images
    """
    def __init__(self, url):
        self.url = url

    def initialize_db(self):
        db = self.__get_db()
        with open('database/schema.sql', 'r') as schema:
            db.cursor().execute(schema.read())
        db.commit()

    def __get_db(self):
        """
        Return open database connection
        :return: open database connection
        """
        connection = sqlite3.connect(self.url)
        connection.row_factory = lambda cursor, row: dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
        return connection

    def __query_db(self, query, args=(), one=False):
        """
        Query database and return collected data
        :param query:
        :param args:
        :param one:
        :return:
        """
        con = self.__get_db()
        cur = con.execute(query, args)
        rv = cur.fetchall()
        con.commit()
        con.close()
        return (rv[0] if rv else None) if one else rv

    def create_task(self, values):
        """
        Create new task in the database
        :param values: (id, url, data_type, tag, active)
        """
        id = str(uuid.uuid1())
        self.__query_db('INSERT INTO tasks VALUES (?, ?, ?, ?, ?)', (id, *values))
        return id

    def update_task(self, id, new_state):
        """
        :param new_state:
        :return:
        """
        self.__query_db('UPDATE tasks set active=? where id=?', (new_state, id))

    def get_tasks_collection(self, url):
        """
        :param url:
        :return:
        """
        if url:
            return self.__query_db("SELECT * FROM tasks WHERE url=?", (url,))
        else:
            return self.__query_db("SELECT * FROM tasks")

    def get_task(self, uuid):
        """
        Return task
        :param uuid: uuid of task to fetch
        :return: dict with task info
        """
        return self.__query_db("SELECT id, url, data_type, tag, active FROM tasks WHERE id=?", (uuid,), one=True)

    def get_image(self, id):
        """
        Return image
        :param id: id of image to fetch
        :return: dict with image info
        """
        return self.__query_db("SELECT id, url, tag FROM images WHERE id=?", (id,), one=True)

    def delete_image(self, id):
        """
        Delete image
        :param id: id of text to delete
        """
        return self.__query_db("DELETE FROM images WHERE id=?", (id,))

    def get_text(self, id):
        """
        Return text
        :param id: id of text to fetch
        :return: dict with text info
        """
        return self.__query_db("SELECT id, url, tag FROM texts WHERE id=?", (id,), one=True)

    def delete_text(self, id):
        """
        Delete text
        :param id: id of text to delete
        """
        return self.__query_db("DELETE FROM texts WHERE id=?", (id,))

    def get_image_content(self, id):
        """
        Return image content
        :param id: id of image content to fetch
        :return: byte data of image content
        """
        return self.__query_db("SELECT content FROM images WHERE id=?", (id,), one=True)

    def get_text_content(self, id):
        """
        Return text content
        :param id: id of text content to fetch
        :return: text content
        """
        return self.__query_db("SELECT content FROM texts WHERE id=?", (id,), one=True)

    def save_data(self, data, url, tag, table):
        """
        Store given data into images table
        :param data: image data
        :param url: image url
        :param tag: image tag
        """
        self.__query_db('INSERT INTO {}(url, tag, content) VALUES (?, ?, ?)'.format(table.replace('"', '""')), (url, tag, data))

    def get_images_collection(self, url, tag):
        """
        Return images from the database
        """
        if url and tag:
            return self.__query_db("SELECT id, tag, url FROM images WHERE url=? and tag='?'", (url, tag))
        elif url:
            return self.__query_db("SELECT id, tag, url FROM images WHERE url=?", (url,))
        elif tag:
            return self.__query_db("SELECT id, tag, url FROM images WHERE tag=?", (tag,))
        else:
            return self.__query_db("SELECT id, tag, url FROM images")

    def get_texts_collection(self, url, tag):
        """
        :param url:
        :param tag:
        :return:
        """
        if url and tag:
            return self.__query_db("SELECT id, tag, url FROM texts WHERE url='?' and tag='?'", (url, tag))
        elif url:
            return self.__query_db("SELECT id, tag, url FROM texts WHERE url='?'", url)
        elif tag:
            return self.__query_db("SELECT id, tag, url FROM texts WHERE tag='?'",tag)
        else:
            return self.__query_db("SELECT id, tag, url FROM texts")

