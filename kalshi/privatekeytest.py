import requests
import os
import requests
import datetime

from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization

from kalshiutils import sign_pss_text, load_private_key_from_file

load_dotenv()
private_key = os.getenv('KALSHI_ACCESS_KEY')



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
