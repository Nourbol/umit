import requests
import json


def post_code(code):
    url = f"http://bazarjok-group.com:60000/user/code/{code}"
    response = requests.post(url, verify=False)
    if response.status_code == 200:
        return response.text
    return None


def get_avatar(token):
    url = f"http://bazarjok-group.com:60000/avatars"
    response = requests.get(url, headers={'Authorization': "Bearer " + token})
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def get_user(token):
    url = f"http://bazarjok-group.com:60000/user"
    response = requests.get(url, headers={'Authorization': "Bearer " + token})
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def get_nearest(token, longitude, latitude):
    url = f"http://bazarjok-group.com:60000/spots/nearest?Longitude={longitude}&Latitude={latitude}"
    response = requests.get(url, headers={'Authorization': "Bearer " + token})
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def get_comments(token, spot_id):
    url = f"http://bazarjok-group.com:60000/api/spots/{spot_id}/comments"
    response = requests.get(url, headers={'Authorization': "Bearer " + token})
    if response.status_code == 200:
        return json.loads(response.text)
    return None
