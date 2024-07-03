from typing import Any, Dict, Optional
from http import HTTPStatus
from typing_extensions import Annotated, Doc
from fastapi.exceptions import HTTPException


class ObjectNotFound(HTTPException):

    def __init__(self, detail: str, headers: Dict[str, str] | None = None) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, detail, headers)

class JobClientError(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code, detail, headers)
    
class USAJobClientManagementError(HTTPException):
    """
    Exception for when things go wrong with USA jobs requests
    """

    def __init__(self, status_code: int, message: str, headers: Optional[Dict] =  None) -> None:
        """
        Constructs USA Management Client Error

        Arguments:
            status_code: Http status code.
            message: Exception message.
            headers: Extra headers
        """
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

    def __str__(self) -> str:
        return f"ERROR_CODE: {self.status_code}::ERROR_MESSAGE: {self.message}"


class USAManagementJsonError(USAJobClientManagementError):
    """
    Exception for when things go wrong with USA Management json response.
    """

    def __init__(self, message: str = "Could not decode response to JSON.") -> None:
        """
        Constructs USA Management Client Error

        Arguments:
            message: Exception message.
        """
        self.status_code = HTTPStatus.BAD_REQUEST.value
        self.message = message
        super().__init__(self.status_code, message)

    def __str__(self) -> str:
        return f"ERROR_CODE: {self.status_code}::ERROR_MESSAGE: {self.message}"