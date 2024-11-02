import unittest

from .. import init_app
from ..patches import PATCHES_PREFIX
from ..vulnerabilities import VULNERABILITIES_PREFIX, ssrf_lfi


class Ssrf1Tests(unittest.TestCase):
    def setUp(self):
        self.test_client = init_app().test_client()
        self.first_hint = ssrf_lfi.FIRST_HINT
        submit_api_path = "/ssrf2/submit_api_url/"
        self.patched_submit_api_path = f"{PATCHES_PREFIX}{submit_api_path}"
        self.vulnerable_submit_api_path = f"{VULNERABILITIES_PREFIX}{submit_api_path}"

    def test_empty_custom_url_returns_400(self):
        response = self.test_client.post(self.patched_submit_api_path, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        response = self.test_client.post(self.vulnerable_submit_api_path, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_first_hint_patched_endpoint_returns_400(self):
        data = {"custom_url": "http://127.0.0.1"}
        response = self.test_client.post(self.patched_submit_api_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

        data = {"custom_url": "http://localhost"}
        response = self.test_client.post(self.patched_submit_api_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_first_hint_vulnerable_endpoint_returns_202(self):
        data = {"custom_url": "file://127.0.0.1"}
        response = self.test_client.post(self.vulnerable_submit_api_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.decode("utf-8"), ssrf_lfi.FIRST_HINT)

        data = {"custom_url": "file://localhost"}
        response = self.test_client.post(self.vulnerable_submit_api_path, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.decode("utf-8"), ssrf_lfi.FIRST_HINT)


# to do: add unit tests for invalid url and successful case
