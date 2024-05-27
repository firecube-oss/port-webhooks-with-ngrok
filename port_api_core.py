import requests
from loguru import logger

# worst implemntation ever :(

PORT_API_BASE_URL = "https://api.getport.io/v1"
PORT_API_TOKEN_URL = f"{PORT_API_BASE_URL}/auth/access_token"

PORT_API_HEADERS = {}

CLIENT_ID = ""
CLIENT_SECRET = ""
raw_response = requests.post(
    f"{PORT_API_BASE_URL}/auth/access_token",
    json={"clientId": CLIENT_ID, "clientSecret": CLIENT_SECRET},
)
# no response from auth API means subsequent calls won't work
if raw_response.status_code > 300:
    logger.error("API Returned a Non 200 Response")
    exit(1)

PORT_API_HEADERS = {
    "Authorization": f"Bearer {raw_response.json().get('accessToken')}",
    "Content-type": "application/json",
}
if PORT_API_HEADERS.get("Authorization") is None:
    logger.error("Unable to add auth Token to Headers")
    exit(1)
