from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# Load private key once
with open("private.pem", "rb") as f:
    PRIVATE_KEY = serialization.load_pem_private_key(
        f.read(),
        password=None
    )


def decrypt_password(encrypted_password: str) -> str:
    """
    Frontend se aaya hua base64 encrypted password decrypt karega
    """

    encrypted_bytes = base64.b64decode(encrypted_password)

    decrypted = PRIVATE_KEY.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode("utf-8")