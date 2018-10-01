import unittest
from todoFlask import app


app.testing = True


class todoFlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_no_todos(self):
        response = self.app.get('/todo')
        self.assertEqual(response.data, b"No todos found!")


if __name__ == "__main__":
    unittest.main()
