from enum import Enum
from typing import Union

from pydantic import BaseModel

from app.utils import errors as err


class CaseInsensitiveEnum(str, Enum):
    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class AllowedFormats(CaseInsensitiveEnum):
    text = "text"
    auth = "authentication"
    structured = "structured"
    binary = "binary"
    location = "location"
    generic = "generic"


class NLIP_SubMessage(BaseModel):
    format: AllowedFormats
    subformat: str
    content: str


class NLIP_Message(BaseModel):
    control: bool
    format: str
    subformat: str
    content: Union[str, dict]
    submessages: list[NLIP_SubMessage] = list()


class NLIP_Exception(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NLIP Exception: {self.message}"


def nlip_encode_text(message: str, control=False, language="english"):
    return NLIP_Message(
        control=control, format=AllowedFormats.text, subformat=language, content=message
    )


def nlip_encode_dict(contents: dict, control=False):
    return NLIP_Message(
        control=control,
        format=AllowedFormats.structured,
        subformat="json",
        content=contents,
    )


def nlip_encode_exception(err: Exception):
    return NLIP_Message(
        control=True,
        format="text",
        subformat="English",
        content=f"Sorry, I can not process your request!! {err}",
    )


def collect_text(msg: NLIP_Message, language: str = "english"):
    answer: str = ""
    if AllowedFormats.text == msg.format:
        if msg.subformat.lower() == language.lower():
            answer = msg.content
    for submsg in msg.submessages:
        if (
            AllowedFormats.text == msg.format
            and msg.subformat.lower() == language.lower()
        ):
            answer = answer + msg.content
    return answer


class NLIP_Session:
    def start(self):
        raise err.UnImplementedError("start", self.__class__.__name__)

    def execute(self, msg: NLIP_Message) -> NLIP_Message:
        raise err.UnImplementedError("start", self.__class__.__name__)

    def stop(self):
        raise err.UnImplementedError("stop", self.__class__.__name__)


class NLIP_Application:
    def startup(self):
        raise err.UnImplementedError("startup", self.__class__.__name__)

    def shutdown(self):
        raise err.UnImplementedError("shutdown", self.__class__.__name__)

    def create_session(self) -> NLIP_Session:
        raise err.UnImplementedError("shutdown", self.__class__.__name__)
