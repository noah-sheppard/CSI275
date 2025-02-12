"""Lab 4, Creating a UDP Socket.

Author: Noah Sheppard
Class: CSI-275-01
Assignment: Lab 4: UDP Sockets

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket
import constants
import random

"""Student code for Lab/HW 2.

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
"""


class TimeOutError(Exception):
    """Used for timeout exceptions."""

    pass


class UDPClient:
    """A UDP client for sending messages to a server."""

    def __init__(self, host, port, use_request_id=False):
        """Initialize the UDP client.

        Args:
            host (str): The hostname or IP address of the server.
            port (int): The UDP port number of the server.
            use_request_id (bool): Whether to use request IDs in messages.
        """
        self.host = host
        self.port = port
        self.use_request_id = use_request_id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(constants.INITIAL_TIMEOUT)

    def send_message_by_character(self, message):
        """Send a message to the server.

        Args:
            message (str): The message to send.

        Returns:
            str: The response from the server.

        Raises:
            TimeOutError: If timeout is reached.
        """
        result = ""
        for char in message:
            timeout = constants.INITIAL_TIMEOUT
            while timeout <= constants.MAX_TIMEOUT:
                try:
                    if self.use_request_id:
                        request_id = random.randint(0, constants.MAX_ID)
                        data = f"{request_id}|{char}".encode('ascii')
                    else:
                        data = char.encode('ascii')

                    self.sock.sendto(data, (self.host, self.port))
                    response, _ = self.sock.recvfrom(constants.MAX_BYTES)
                    response = response.decode('ascii')

                    if self.use_request_id:
                        response_id, response_char = response.split('|')
                        if int(response_id) == request_id:
                            result += response_char
                            break
                    else:
                        result += response
                        break
                except socket.timeout:
                    timeout *= 2
                    self.sock.settimeout(timeout)
            else:
                raise TimeOutError("Max timeout")
        return result


def main():
    """Run some basic tests on the required functionality.

    For more extensive tests, run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
