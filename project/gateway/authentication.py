import os.path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


class AuthenticationCenter:
    def __init__(self, private_key_path: str, public_key_path: str,
                 password: str) -> None:
        self.password = password.encode('utf-8')
        self.private_key = None

        if os.path.exists(private_key_path):
            self.load_private_key(private_key_path)
        else:
            self.generate_private_key(private_key_path)
            self.generate_public_key(public_key_path)

    def generate_private_key(self, path: str) -> None:
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(path, "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"Qwerty123")
            ))

        print(f"Generated new private key at {path}")

    def generate_public_key(self, path: str) -> None:
        pub_key = self.private_key.public_key()

        with open(path, "wb") as f:
            f.write(pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        print(f"Generated new public key at {path}")

    def load_private_key(self, path: str) -> None:
        with open(path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=self.password,
                backend=default_backend()
            )

    def signature(self, message: bytes) -> bytes:
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
