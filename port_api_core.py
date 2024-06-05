from time import time

from loguru import logger
from pydantic import BaseModel, Field, HttpUrl, PrivateAttr
from requests import delete, get, patch, post, put
from requests.models import Response


def get_time(seconds_precision: bool = True) -> float:
    return time() if not seconds_precision else int(time())


# https://api.getport.io/static/index.html#/Authentication%20%2F%20Authorization/post_v1_auth_access_token
class PortAuthAccessTokenRequest(BaseModel):
    client_id: str = Field(serialization_alias="clientId")
    client_secret: str = Field(serialization_alias="clientSecret")


class PortAuthAccessTokenResponse(BaseModel):
    ok: bool
    access_token: str = Field(validation_alias="accessToken")
    expires_in: int = Field(validation_alias="expiresIn")
    token_type: str = Field(validation_alias="tokenType")
    _retrieved_time: int = PrivateAttr(default_factory=lambda: int(get_time()))

    @property
    def expired(self) -> bool:
        return self._retrieved_time + self.expires_in < get_time()

    @property
    def full_token(self) -> str:
        return f"{self.token_type} {self.access_token}"


class PortClient:
    API_HEADERS = {
        "Authorization": "",
        "Content-type": "application/json",
    }
    API_BASE_URL = "https://api.getport.io/v1"

    def __init__(self, exclude_pydantic_fields: str = "") -> None:
        self._exclude_pydantic_fields = exclude_pydantic_fields

    @classmethod
    def authenticate(cls, auth_request: PortAuthAccessTokenRequest):
        API_TOKEN_URL = f"{cls.API_BASE_URL}/auth/access_token"
        raw_response = post(API_TOKEN_URL, json=auth_request.model_dump(by_alias=True))
        if raw_response.status_code == 200:
            token_response = PortAuthAccessTokenResponse.model_validate(
                raw_response.json()
            )
            cls.API_HEADERS["Authorization"] = token_response.full_token
            logger.info(
                f"Obtained a Port Token valid for {round(token_response.expires_in / 3600,2)} Hours"
            )

        # no response from auth API means subsequent calls won't work
        if raw_response.status_code > 200:
            logger.error("Port Authentication API Returned a Non 200 Response")
            exit(1)

    def process_port_api_response(self, raw_response: Response):
        if (
            raw_response.status_code < 300
            and "application/json" in raw_response.headers["Content-Type"]
        ):
            logger.info("API Call Successful")
            return raw_response.json()
        else:
            logger.error(
                f"Status Code: {raw_response.status_code} \n Message: {raw_response.text} \n Returned Content-Type: {raw_response.headers['Content-Type']}"
            )
            return None

    def prepare_body(self, body) -> str:
        return body.model_dump_json(
            exclude_none=True, exclude=self._exclude_pydantic_fields
        )

    def post(self, body: str, url: HttpUrl):
        raw_response = post(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        return self.process_port_api_response(raw_response)

    def get(self, url: HttpUrl) -> dict:
        raw_response = get(url=url, headers=self.__class__.API_HEADERS)
        return self.process_port_api_response(raw_response)

    def patch(self, body: str, url: HttpUrl):
        raw_response = patch(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        return self.process_port_api_response(raw_response)

    def delete(self, body: str, url: HttpUrl):
        raw_response = delete(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        return self.process_port_api_response(raw_response)

    def put(self, body: str, url: HttpUrl):
        raw_response = put(
            url=url, data=self.prepare_body(body), headers=self.__class__.API_HEADERS
        )
        return self.process_port_api_response(raw_response)
