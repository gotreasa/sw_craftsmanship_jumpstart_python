"""pact tests for dummy app"""

import logging
import os

import pytest
import requests
from pact import Consumer, Provider, Format

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
print(Format().__dict__)

PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope="session")
def pact():
    pact = Consumer("dummy-consumer").has_pact_with(
        Provider("dummy-provider"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir="./pacts",
        log_dir="./logs",
    )
    try:
        print("start service")
        pact.start_service()
        yield pact
    finally:
        print("stop service")
        pact.stop_service()


def test_get_health_endpoint(pact):
    expected = {}
    (
        pact.given("a running app")
        .upon_receiving("a request to get the health of the service")
        .with_request("GET", "/health")
        .will_respond_with(200, body=expected)
    )
    with pact:
        result = requests.get(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}/health")
    assert result.json() == expected
    assert result.status_code == 200


def test_get_dummy_endpoint(pact):
    expected = {}
    (
        pact.given("a running app")
        .upon_receiving("a request to get the dummy endpoint")
        .with_request("GET", "/1.0.0/dummy")
        .will_respond_with(200, body=expected)
    )
    with pact:
        result = requests.get(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}/1.0.0/dummy")
    assert result.json() == expected
    assert result.status_code == 200
