import logging
import os
from os import getenv
from subprocess import call

from . import AbstractHandler


class K8sHandler(AbstractHandler):

    def __init__(self, logger=None):
        """
            Concrete implementation of the Kubernetes handler.
        """
        self.logger = logger or logging.getLogger(__name__)
        if 'NODE_NAME' in os.environ:
            self.node_name = getenv('NODE_NAME')
        else:
            self.logger.error('NODE_NAME env variable not set')
            self.node_name = '<empty-name>'
        self.drain_parameters = getenv(
            'DRAIN_PARAMETERS', '--grace-period=120 --force --ignore-daemonsets',
        )

    def run(self):
        """
            Run Kubernetes handler
        """
        kube_command = ['kubectl', 'drain', self.node_name]
        kube_command += self.drain_parameters.split()
        self.logger.info('Draining node: %s' % self.node_name)
        try:
            self.logger.debug('Calling: %s', ' '.join(kube_command))
            result = call(kube_command)
            if result == 0:
                self.logger.info('Node Drain successful')
        except BaseException:
            self.logger.error(
                'Kubectl command failed: %s',
                ' '.join(kube_command),
            )
            pass
