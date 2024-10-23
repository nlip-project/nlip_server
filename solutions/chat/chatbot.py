import os

from fastapi import Response

from app.schemas import nlip
from app.schemas.genai import StatefulGenAI
from app.server import setup_server


class ChatApplication(nlip.NLIP_Application):
    def startup(self):
        self.model = os.environ.get("CHAT_MODEL", "mistral")
        self.host = os.environ.get("CHAT_HOST", "localhost")
        self.port = os.environ.get("CHAT_PORT", 11434)

    def shutdown(self):
        return None

    def create_session(self) -> nlip.NLIP_Session:
        return ChatSession(host=self.host, port=self.port, model=self.model)


class ChatSession(nlip.NLIP_Session):

    def __init__(self, host: str, port: int, model: str):
        self.host = host
        self.port = port
        self.model = model

    def start(self):
        self.server = StatefulGenAI(self.host, self.port, self.model)

    def execute(self, msg: nlip.NLIP_Message) -> nlip.NLIP_Message:
        text = nlip.collect_text(msg)
        response = self.server.chat(text)
        return nlip.nlip_encode_text(response)

    def stop(self):
        self.server = None


app = setup_server(ChatApplication())
