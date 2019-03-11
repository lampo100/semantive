import unittest

from app import app

client = app.test_client()

class TestService(unittest.TestCase):
    def test_get_scraping_tasks(self):
        r = client.get('/api/scraping-tasks/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_post_scraping_tasks(self):
        r = client.post('/api/scraping-tasks/', base_url='https://localhost')
        self.assertEqual(r.status_code, 201)

    def test_put_scraping_tasks(self):
        r = client.put('/api/scraping-tasks/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_get_scraping_task_by_id(self):
        r = client.get('/api/scraping-tasks/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_delete_scraping_task_by_id(self):
        r = client.delete('/api/scraping-tasks/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 204)

    def test_put_scraping_task_by_id(self):
        r = client.put('/api/scraping-tasks/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 204)

    def test_get_images(self):
        r = client.get('/api/images/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_get_image_by_id(self):
        r = client.get('/api/images/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_delete_image_by_id(self):
        r = client.delete('/api/images/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 204)

    def test_get_image_content(self):
        r = client.get('/api/images/22/content', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_get_texts(self):
        r = client.get('/api/texts/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_get_text_by_id(self):
        r = client.get('/api/texts/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)

    def test_delete_text_by_id(self):
        r = client.delete('/api/texts/22/', base_url='https://localhost')
        self.assertEqual(r.status_code, 204)

    def test_get_text_content(self):
        r = client.get('/api/texts/22/content', base_url='https://localhost')
        self.assertEqual(r.status_code, 200)
