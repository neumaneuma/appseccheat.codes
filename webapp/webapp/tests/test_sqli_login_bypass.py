import unittest

from .. import init_app
from ..patches import PATCHES_PREFIX
from ..vulnerabilities import VULNERABILITIES_PREFIX


class Sqli1Tests(unittest.TestCase):
    def setUp(self):
        self.test_client = init_app().test_client()
        login_path = "/sqli1/login/"
        self.patched_login_path = f"{PATCHES_PREFIX}{login_path}"
        self.vulnerable_login_path = f"{VULNERABILITIES_PREFIX}{login_path}"

    def test_empty_username_and_password_returns_401(self):
        response = self.test_client.post(self.patched_login_path, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        response = self.test_client.post(self.vulnerable_login_path, follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_empty_username_returns_401(self):
        data = {"password": "password"}
        response = self.test_client.post(self.patched_login_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        response = self.test_client.post(self.vulnerable_login_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_empty_password_returns_401(self):
        data = {"username": "username"}
        response = self.test_client.post(self.patched_login_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        response = self.test_client.post(self.vulnerable_login_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
