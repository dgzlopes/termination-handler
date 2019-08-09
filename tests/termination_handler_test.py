import pytest   # noqa: F401
import requests   # noqa: F401
import responses

from termination_handler.termination_handler import check_status

def test_check_bad_status():
    assert check_status('aws') is False
    assert check_status('gcp') is False

def test_check_unknown_provider_status():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_status('unknown')
    assert pytest_wrapped_e.type == SystemExit

@responses.activate
def test_response_aws_check():
    mocking_url = 'http://169.254.169.254/latest/meta-data/spot/termination-time'
    responses.add(
        responses.GET, mocking_url,
    )

    assert check_status('aws') is True

@responses.activate
def test_bad_response_aws_check():
    mocking_url = 'http://169.254.169.254/latest/meta-data/spot/termination-time'
    responses.add(
        responses.GET, mocking_url, status=404,
    )

    assert check_status('aws') is False

@responses.activate
def test_response_gcp_check():
    mocking_url = 'http://metadata.google.internal/computeMetadata/v1/instance/preempted'
    headers = {'Metadata-Flavor': 'Google'}
    responses.add(
        responses.GET, mocking_url, headers=headers, body='TRUE'
    )

    assert check_status('gcp') is True

@responses.activate
def test_negative_response_gcp_check():
    mocking_url = 'http://metadata.google.internal/computeMetadata/v1/instance/preempted'
    headers = {'Metadata-Flavor': 'Google'}
    responses.add(
        responses.GET, mocking_url, headers=headers, body='FALSE'
    )
        
    assert check_status('gcp') is False