from pydantic import  BaseModel

from port_api_core import PortClient


# base model for for requests going to Actions API
class PortActionsRequestBase(BaseModel):
    pass

class PortActionsClient:
    def __init__(self, action_identifier) -> None:
        self._client = PortClient(exclude_pydantic_fields="action_identifier")
        self._API_URL = f"{PortClient.API_BASE_URL}/actions/{action_identifier}"
        self._action_identifier = action_identifier
