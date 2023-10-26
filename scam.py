import requests


async def is_have(url):
    try:
        requests.get(url)
        return True
    except requests.exceptions.ConnectionError:
        return False


async def bitdefender_check(url):  # Bitdefender TrafficLight
    endpoint = "https://nimbus.bitdefender.net/url/status"
    payload = {
        "url": url
    }
    response = requests.post(url= endpoint, json=payload)
    response = response.json()
    if response['status_code'] == 0:
        return True
    else:
        return False



