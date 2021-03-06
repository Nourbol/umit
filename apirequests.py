import requests
import json


def post_code(code):
    url = f"http://bazarjok-group.com:60000/user/code/{code}"
    response = requests.post(url, verify=False)
    if response.status_code == 200:
        return response.text
    return None


def get_avatar():
    url = f"http://bazarjok-group.com:60000/avatars"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def set_avatar(token, avatar_id):
    url = f"http://bazarjok-group.com:60000/user"
    body = {
        "avatarId": avatar_id
    }
    response = requests.patch(url, data=json.dumps(body, ensure_ascii=False)
                              .encode('utf-8'), headers=
                              {
                                  'Authorization': "Bearer " + token,
                                  "Content-Type": "application/json"
                              })
    if response.status_code == 200:
        return 'ok'
    else:
        return response.text


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


def send_comment(token, spot_id, text, longitude, latitude):
    body = {
        "text": text,
        "longitude": longitude,
        "latitude": latitude
    }

    url = f"http://bazarjok-group.com:60000/api/spots/{spot_id}/comments"
    response = requests.post(url, data=json.dumps(body, ensure_ascii=False)
                             .encode('utf-8'), headers=
                             {
                                 'Authorization': "Bearer " + token,
                                 "Content-Type": "application/json"
                             })
    if response.status_code == 200:
        return 'ok'
    else:
        return response.text


def post_likes(token, spot_id, comment_id):
    url = f"http://bazarjok-group.com:60000/spots/{spot_id}/comments/{comment_id}/likes"
    response = requests.post(url, headers={'Authorization': "Bearer " + token})
    if response.status_code == 204:
        return "ok"
    return None


def get_users_comments(token):
    url = "http://bazarjok-group.com:60000/api/comments"
    response = requests.get(url, headers={'Authorization': "Bearer " + token})
    if response.status_code == 200:
        return json.loads(response.text)
    return None
