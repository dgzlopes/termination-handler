from __future__ import generators

import argparse
import logging
import os
import sys
import time

import requests
from cloud_detect import provider

from termination_handler.handlers import K8sHandler
from termination_handler.handlers import NomadHandler


def parse_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(
        description='',
    )
    parser.add_argument(
        '-w',
        '--wait',
        metavar='w',
        nargs='?',
        default=60,
        type=float,
        help='(seconds, %(type)s, default: %(default)s)',
    )
    parser.add_argument(
        '-s',
        '--step',
        metavar='s',
        nargs='?',
        default=5,
        type=float,
        help='(seconds, %(type)s, default: %(default)s)',
    )
    parser.add_argument(
        '--k8s',
        default=os.environ.get('K8S_TERMINATION_HANDLER'),
        action='store_true',
        help='draining of Kubernetes nodes',
    )
    parser.add_argument(
        '--nomad',
        default=os.environ.get('NOMAD_TERMINATION_HANDLER'),
        action='store_true',
        help='draining of Nomad nodes',
    )
    parser.add_argument(
        '--demo',
        default=os.environ.get('DEMO_TERMINATION_HANDLER'),
        action='store_true',
        help='runs all the activated handlers (useful for testing)',
    )
    return parser.parse_args()


def check_status(provider=None):
    """ Return checking function for the passed provider"""
    if provider == 'aws':
        return check_aws()
    elif provider == 'gcp':
        return check_gcp()
    else:
        logging.error('Nothing to check')
        sys.exit()


def check_aws():
    """ Check if AWS termination notice exists """
    base_url = 'http://169.254.169.254/latest/meta-data/spot'
    url = base_url + '/termination-time'
    try:
        if requests.get(url, timeout=2).status_code == 200:
            return True
    except BaseException:
        pass
    return False


def check_gcp():
    """ Check if GCP termination notice exists """
    base_url = 'http://metadata.google.internal/computeMetadata/v1/instance'
    headers = {'Metadata-Flavor': 'Google'}
    url = base_url + '/preempted'
    try:
        if requests.get(url, headers=headers, timeout=2).text == 'TRUE':
            return True
    except BaseException:
        pass
    return False


def build_handlers(args):
    """ Builds all the handlers passed and returns a list of them """
    handlers_to_return = []
    if args.k8s:
        handlers_to_return.append(K8sHandler())
    if args.nomad:
        handlers_to_return.append(NomadHandler())
    return handlers_to_return


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_arguments()
    logging.info('Discovering cloud provider')
    cloud_provider_name = provider()
    logging.info('Building handlers')
    handler_list = build_handlers(args)

    wait_time = args.wait
    wait_step = args.step
    logging.info(
        'Running termination-handler with wait_time %d and wait_step %d on %s ',
        wait_time, wait_step, cloud_provider_name,
    )
    if cloud_provider_name != 'unknown' and args.demo is not True:
        count = 0
        while True:
            if check_status(cloud_provider_name) is True:
                logging.info('Preemption started')
                for handler in handler_list:
                    handler.run()
                break
            else:
                if count == wait_time:
                    logging.info('Waiting for notice')
                    count = 0
                count += wait_step
                time.sleep(wait_step)
    else:
        if args.demo:
            logging.info('Running demo mode. Executing handlers')
            for handler in handler_list:
                handler.run()
            sys.exit()
        else:
            logging.error(
                "Run failed. Cloud provider '%s' not valid", cloud_provider_name,
            )
            sys.exit()
