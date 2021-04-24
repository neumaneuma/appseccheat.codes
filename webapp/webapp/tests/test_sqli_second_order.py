from unittest.mock import patch
import unittest

from . import SECRET_KEY
from . import cookie_helper
from .. import init_app
from ..vulnerabilities import sqli_second_order
from ..vulnerabilities import VULNERABILITIES_PREFIX
from ..patches import PATCHES_PREFIX


class Sqli2Tests(unittest.TestCase):
    def setUp(self):
        self.test_client = init_app().test_client()
        self.session_cookie_name = "session"
        self.secret_key = SECRET_KEY
        self.username_cookie = sqli_second_order.username_to_exploit
        self.user_id_cookie = sqli_second_order.user_id_for_registered_account

        get_username_path = "/sqli2/get_username/"
        register_path = "/sqli2/register/"
        change_password_path = "/sqli2/change_password/"
        self.patched_get_username_path = f"{PATCHES_PREFIX}{get_username_path}"
        self.patched_register_path = f"{PATCHES_PREFIX}{register_path}"
        self.patched_change_password_path = f"{PATCHES_PREFIX}{change_password_path}"
        self.vulnerable_get_username_path = (
            f"{VULNERABILITIES_PREFIX}{get_username_path}"
        )
        self.vulnerable_register_path = f"{VULNERABILITIES_PREFIX}{register_path}"
        self.vulnerable_change_password_path = (
            f"{VULNERABILITIES_PREFIX}{change_password_path}"
        )

    def test_get_username(self):
        response = self.test_client.get(self.patched_get_username_path)
        self.assertEqual(response.status_code, 200)
        response = self.test_client.get(self.vulnerable_get_username_path)
        self.assertEqual(response.status_code, 200)

    def test_register_empty_username_and_password_returns_401(self):
        response = self.test_client.post(
            self.patched_register_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)
        response = self.test_client.post(
            self.vulnerable_register_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)

    def test_register_empty_username_returns_401(self):
        data = {"password": "password"}
        response = self.test_client.post(
            self.patched_register_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)
        response = self.test_client.post(
            self.vulnerable_register_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)

    def test_register_empty_password_returns_401(self):
        data = {"username": "username"}
        response = self.test_client.post(
            self.patched_register_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)
        response = self.test_client.post(
            self.vulnerable_register_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)

    def test_change_password_no_cookies_400(self):
        response = self.test_client.post(
            self.patched_change_password_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        response = self.test_client.post(
            self.vulnerable_change_password_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_change_password_username_cookie_missing_400(self):
        cookies = {self.user_id_cookie: "test"}
        session_cookie = cookie_helper.encode_flask_cookie(self.secret_key, cookies)
        self.test_client.set_cookie(
            self.patched_change_password_path, self.session_cookie_name, session_cookie
        )
        response = self.test_client.post(
            self.patched_change_password_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        self.test_client.set_cookie(
            self.vulnerable_change_password_path, self.session_cookie_name, session_cookie
        )
        response = self.test_client.post(
            self.vulnerable_change_password_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_change_password_user_id_cookie_missing_400(self):
        cookies = {self.username_cookie: "test"}
        session_cookie = cookie_helper.encode_flask_cookie(self.secret_key, cookies)
        self.test_client.set_cookie(
            self.patched_change_password_path, self.session_cookie_name, session_cookie
        )
        response = self.test_client.post(
            self.patched_change_password_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        self.test_client.set_cookie(
            self.vulnerable_change_password_path, self.session_cookie_name, session_cookie
        )
        response = self.test_client.post(
            self.vulnerable_change_password_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    # attempting to use unit tests patch decorator results in a module not found error so i need to use this hacky approach for now
    def test_change_password_no_cookies_missing(self):
        cookies = {self.username_cookie: "test", self.user_id_cookie: "test"}
        session_cookie = cookie_helper.encode_flask_cookie(self.secret_key, cookies)
        self.test_client.set_cookie(
            self.patched_change_password_path, self.session_cookie_name, session_cookie
        )
        exception_thrown = False
        try:
            self.test_client.post(
                self.patched_change_password_path, follow_redirects=True
            )
        except:
            exception_thrown = True

        self.assertTrue(exception_thrown)
        self.test_client.set_cookie(
            self.vulnerable_change_password_path, self.session_cookie_name, session_cookie
        )
        exception_thrown = False
        try:
            self.test_client.post(
                self.vulnerable_change_password_path, follow_redirects=True
            )
        except:
            exception_thrown = True

        self.assertTrue(exception_thrown)
