import requests
import json


def post_code(code):
    url = f"http://bazarjok-group.com:60000/user/code/{code}"
    response = requests.post(url, verify=False)
    print(response)
    if response.status_code == 200:
        return response.text
    return None
