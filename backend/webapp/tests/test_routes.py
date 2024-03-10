import unittest
from .. import init_app


class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = init_app().test_client()

    def test_root_path_returns_200(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_faq_path_returns_200(self):
        path = "/faq/"
        response = self.app.get(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_sqli-login-bypass_path_returns_200(self):
        path = "/sqli-login-bypass/"
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_sqli-second-order_path_returns_200(self):
        path = "/sqli-second-order/"
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_ssrf-bypass-webhook_path_returns_200(self):
        path = "/ssrf-bypass-webhook/"
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_ssrf-local-file-inclusion_path_returns_200(self):
        path = "/ssrf-local-file-inclusion/"
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)