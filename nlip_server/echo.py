"""
This is an echo server which simply sends back the message
that is received to the client.

This is used to test that all types of messages can be encoded
and sent back to the client in the right manner.

"""

from nlip_server.server import SafeApplication, NLIP_Session, setup_server
from nlip_sdk.nlip import NLIP_Message


class EchoApplication(SafeApplication):

    def create_session(self) -> NLIP_Session:
        return EchoSession()


class EchoSession(NLIP_Session):
    def execute(
        self, msg: NLIP_Message) -> NLIP_Message:
        self.get_logger().info(f"Got Message {msg}")
        return msg


app = setup_server(EchoApplication())
