from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# defaults
PATH_TO_KEY = "./key.pem"
PASSWORD = "Qwerty123"


class AuthorizationCenter:
    def __init__(self, path=None, password=PASSWORD):
        self.password = password.encode('utf-8')
        self.key = None
        if path:
            self.path = path
            self.load_key()
        else:
            self.path = PATH_TO_KEY
            self.generate_key()

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

    def signature(self, message):
        bytes_msg = message.encode('utf-8')
        signature = self.key.sign(
            bytes_msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
