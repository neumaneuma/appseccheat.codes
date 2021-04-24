# Adapted from https://gist.github.com/aescalana/7e0bc39b95baa334074707f73bc64bfe

from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer


class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    def get_signing_serializer(self, secret_key):
        signer_kwargs = {
            "key_derivation": self.key_derivation,
            "digest_method": self.digest_method,
        }
        return URLSafeTimedSerializer(
            secret_key,
            salt=self.salt,
            serializer=self.serializer,
            signer_kwargs=signer_kwargs,
        )


def decode_flask_cookie(secret_key, cookieValue):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.loads(cookieValue)


def encode_flask_cookie(secret_key, cookies):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.dumps(cookies)
