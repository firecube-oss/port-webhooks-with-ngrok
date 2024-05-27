from typing import Any

import requests
from loguru import logger
from pydantic import BaseModel


# https://api.getport.io/static/index.html#/Authentication%20%2F%20Authorization/post_v1_auth_access_token
class PortAuthAccessTokenRequest(BaseModel):
    clientId: str
    clientSecret: str


class PortAuthAccessTokenResponse(BaseModel):
    ok: bool
    accessToken: str
    expiresIn: int
    tokenType: str


class PortClient:
    API_HEADERS = {
        "Authorization": "",
        "Content-type": "application/json",
    }
    API_BASE_URL = "https://api.getport.io/v1"
    API_TOKEN_URL = f"{API_BASE_URL}/auth/access_token"

    def __init__(self) -> None:
        pass

    @classmethod
    def authenticate(cls, clientId: str, clientSecret: str):
        auth_request = PortAuthAccessTokenRequest(
            clientId=clientId, clientSecret=clientSecret
        )

        raw_response = requests.post(
            cls.API_TOKEN_URL, json=auth_request.model_dump()
        )

        if raw_response.status_code == 200:
            token_response = PortAuthAccessTokenResponse.model_validate(
                raw_response.json()
            )
            cls.API_HEADERS["Authorization"] = (
                f"{token_response.tokenType} {token_response.accessToken}"
            )
            logger.info(f"Obtained a Port Token valid for {token_response.expiresIn}")

        # no response from auth API means subsequent calls won't work
        if raw_response.status_code > 200:
            logger.error("Port Authentication API Returned a Non 200 Response")
            exit(1)
