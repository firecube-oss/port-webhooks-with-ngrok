from loguru import logger
from pydantic import BaseModel, HttpUrl
from requests import delete, get, patch, post, put
from requests.models import Response


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

    def __init__(self, exclude_pydantic_fields: str = "" ) -> None:
        self._exclude_pydantic_fields = exclude_pydantic_fields

    @classmethod
    def authenticate(cls, clientId: str, clientSecret: str):
        API_TOKEN_URL = f"{cls.API_BASE_URL}/auth/access_token"
        auth_request = PortAuthAccessTokenRequest(
            clientId=clientId, clientSecret=clientSecret
        )

        raw_response = post(API_TOKEN_URL, json=auth_request.model_dump())

        if raw_response.status_code == 200:
            token_response = PortAuthAccessTokenResponse.model_validate(
                raw_response.json()
            )
            cls.API_HEADERS["Authorization"] = (
                f"{token_response.tokenType} {token_response.accessToken}"
            )
            logger.info(
                f"Obtained a Port Token valid for {round(token_response.expiresIn / 3600,2)} Hours"
            )

        # no response from auth API means subsequent calls won't work
        if raw_response.status_code > 200:
            logger.error("Port Authentication API Returned a Non 200 Response")
            exit(1)

    def log_port_api_response(self, raw_response: Response):
        if raw_response.status_code < 300 and "application/json" in raw_response.headers["Content-Type"]:
            logger.info("API Call Successful")
        else:
            logger.error(
                f"Status Code: {raw_response.status_code} Message: {raw_response.text} Returned Content-Type: {raw_response.headers['Content-Type']}"
            )

    def prepare_body(self, body) -> str:
        return body.model_dump_json(
            exclude_none=True, exclude=self._exclude_pydantic_fields
        )

    def post(self, body: str, url: HttpUrl):
        raw_response = post(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        self.log_port_api_response(raw_response)

    def get(self, url: HttpUrl):
        raw_response = get(url=url, headers=self.__class__.API_HEADERS)
        self.log_port_api_response(raw_response)
        if "application/json" in raw_response.headers["Content-Type"]:
            return raw_response.json()
        else:
            return {}

    def patch(self, body: str, url: HttpUrl):
        raw_response = patch(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        self.log_port_api_response(raw_response)

    def delete(self, body: str, url: HttpUrl):
        raw_response = delete(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        self.log_port_api_response(raw_response)

    def put(self, body: str, url: HttpUrl):
        raw_response = put(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        self.log_port_api_response(raw_response)
