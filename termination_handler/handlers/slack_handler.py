import logging
import socket

import slack

from . import AbstractHandler


def _get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def _get_hostname():
    return socket.gethostname()


class SlackHandler(AbstractHandler):
    """
        Concrete implementation of the Slack handler.
    """

    def __init__(self, token, channel, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.client = slack.WebClient(token=token)
        self.channel = channel

    def run(self):
        """
            Run Slack handler
        """
        # TODO: Add cloud provider to the message
        self.logger.info('Sending message to: %s' % self.channel)
        self.client.chat_postMessage(
            channel=self.channel,
            text='Instance ' + _get_local_ip() + ' with hostname ' +
            _get_hostname() + 'is being terminated.',
        )
