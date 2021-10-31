import requests

def reverse(str):
    return "".join(reversed(str))

def upcase(str):
    response = requests.post(
        "http://api.shoutcloud.io/V1/SHOUT",
        json={"INPUT": str}
    )

    response.raise_for_status()

    return response.json()["OUTPUT"]
