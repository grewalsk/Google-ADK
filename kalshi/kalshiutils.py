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
import json

def export_kalshi_events_to_json(filename="kalshi_events.json"):
    """Fetch Kalshi events and export to JSON file"""
    url = "https://api.elections.kalshi.com/trade-api/v2/events?limit=200&status=open"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()

        # Write to JSON file
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=2, sort_keys=False)

        print(f"Successfully exported {len(data.get('events', []))} events to {filename}")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
export_kalshi_events_to_json()
