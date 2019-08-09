import logging
from os import getenv
from subprocess import call

from . import AbstractHandler


class NomadHandler(AbstractHandler):
    """
        Concrete implementation of the Nomad handler.
    """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.drain_parameters = getenv(
            'DRAIN_PARAMETERS', '-self -force -ignore-system',
        )

    def run(self):
        """
            Run Nomad handler
        """
        nomad_command = ['nomad', 'node', 'drain', '-enable']
        nomad_command += self.drain_parameters.split()

        self.logger.info('Draining node')
        try:
            result = call(nomad_command)
            if result == 0:
                self.logger.info('Node Drain successful')
        except BaseException:
            self.logger.error(
                'Nomad command failed: %s',
                ' '.join(nomad_command),
            )
            pass
