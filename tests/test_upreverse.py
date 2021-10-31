import requests
import requests_mock
from src.upreverse import reverse, upcase

def test_reverse():
    assert reverse('reverse') == 'esrever'

def test_upcase(requests_mock):
    requests_mock.post(
        "http://api.shoutcloud.io/V1/SHOUT",
        json={"OUTPUT": "HELLO"}
    )

    assert upcase("hello") == "HELLO"
