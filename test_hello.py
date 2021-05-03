import unittest

from hello import app


class PageTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_page_renders(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_page_content(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.data.decode('UTF-8'), 'Hello, World!')


if __name__ == "__main__":
    unittest.main()
