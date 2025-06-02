# Fix file imports

import os 
from dotenv import load_dotenv
load_dotenv()


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_private_key_from_file(file_path):
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # or provide a password if your key is encrypted
            backend=default_backend()
        )
    return private_key


import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

def sign_pss_text(private_key: rsa.RSAPrivateKey, text: str) -> str:
    # Before signing, we need to hash our message.
    # The hash is what we actually sign.
    # Convert the text to bytes
    message = text.encode('utf-8')

    try:
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    except InvalidSignature as e:
        raise ValueError("RSA sign PSS failed") from e
import requests
import datetime

# Get the current time
current_time = datetime.datetime.now()

# Convert the time to a timestamp (seconds since the epoch)
timestamp = current_time.timestamp()

# Convert the timestamp to milliseconds
current_time_milliseconds = int(timestamp * 1000)
timestampt_str = str(current_time_milliseconds)

# Load the RSA private key
private_key = os.getenv('KALSHI_ACCESS_KEY')

method = "GET"
base_url = 'https://demo-api.kalshi.co'
path='/trade-api/v2/portfolio/balance'


msg_string = timestampt_str + method + path

private_key_pem_bytes = private_key.encode('utf-8')

kalshi_private_key_object = serialization.load_pem_private_key(
            private_key_pem_bytes,
            password=None, # Or your password if the key is encrypted
        )


sig = sign_pss_text(kalshi_private_key_object, msg_string)

headers = {
        'KALSHI-ACCESS-KEY': os.getenv('KALSHI_API_KEY_ID'),
        'KALSHI-ACCESS-SIGNATURE': sig,
        'KALSHI-ACCESS-TIMESTAMP': timestampt_str
    }
response = requests.get(base_url + path, headers=headers)
print("Status Code:", response.status_code)
print("Response Body:", response.text)
