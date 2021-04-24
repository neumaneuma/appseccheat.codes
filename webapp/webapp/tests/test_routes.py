import unittest
from .. import init_app


class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = init_app().test_client()

    def test_root_path_returns_200(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_faq_path_returns_200(self):
        response = self.app.get("/faq")
        self.assertEqual(response.status_code, 200)

import unittest
from .. import init_app


class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = init_app().test_client()

    def test_root_path_returns_200(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_faq_path_returns_200(self):
        response = self.app.get("/faq")
        self.assertEqual(response.status_code, 200)

    def test_sqli1_path_returns_200(self):
        path = "/sqli1"
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_sqli2_path_returns_200(self):
        path = "/sqli2"
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
