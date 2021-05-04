import unittest
from .. import init_app
from ..vulnerabilities import VULNERABILITIES_PREFIX
from ..vulnerabilities import ssrf_webhook
from ..patches import PATCHES_PREFIX


class Ssrf1Tests(unittest.TestCase):
    def setUp(self):
        self.test_client = init_app().test_client()
        self.first_hint = ssrf_webhook.FIRST_HINT
        self.second_hint = ssrf_webhook.SECOND_HINT
        submit_webhook_path = "/ssrf1/submit_webhook/"
        self.patched_submit_webhook_path = f"{PATCHES_PREFIX}{submit_webhook_path}"
        self.vulnerable_submit_webhook_path = (
            f"{VULNERABILITIES_PREFIX}{submit_webhook_path}"
        )

    def test_empty_custom_url_returns_400(self):
        response = self.test_client.post(
            self.patched_submit_webhook_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        response = self.test_client.post(
            self.vulnerable_submit_webhook_path, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_first_hint_patched_endpoint_returns_400(self):
        data = {"custom_url": "http://127.0.0.1"}
        response = self.test_client.post(
            self.patched_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

        data = {"custom_url": "http://localhost"}
        response = self.test_client.post(
            self.patched_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_first_hint_vulnerable_endpoint_returns_202(self):
        data = {"custom_url": "http://127.0.0.1"}
        response = self.test_client.post(
            self.vulnerable_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.decode("utf-8"), ssrf_webhook.FIRST_HINT)

        data = {"custom_url": "http://localhost"}
        response = self.test_client.post(
            self.vulnerable_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.decode("utf-8"), ssrf_webhook.FIRST_HINT)

    def test_second_hint_vulnerable_endpoint_returns_202(self):
        data = {"custom_url": "http://internal_api"}
        response = self.test_client.post(
            self.vulnerable_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.decode("utf-8"), ssrf_webhook.SECOND_HINT)

        data = {"custom_url": "http://internal_api:80"}
        response = self.test_client.post(
            self.vulnerable_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.decode("utf-8"), ssrf_webhook.SECOND_HINT)

    def test_second_hint_patched_endpoint_returns_400(self):
        data = {"custom_url": "http://internal_api"}
        response = self.test_client.post(
            self.patched_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

        data = {"custom_url": "http://internal_api:80"}
        response = self.test_client.post(
            self.patched_submit_webhook_path, data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
