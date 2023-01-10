from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# defaults
PATH_TO_KEY = "./key.pem"
PASSWORD = b"Qwerty123"


class AuthorizationCenter:
    def __init__(self, path=PATH_TO_KEY, password=PASSWORD):
        self.path = path
        self.key = None
        self.password = password

    def generate_key(self):
        self.key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(self.path, "wb") as f:
            f.write(self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"Qwerty123")
            ))

    def load_key(self):
        with open(self.path, "rb") as f:
            self.key = serialization.load_pem_private_key(
                f.read(),
                password=self.password,
                backend=default_backend()
            )
