from .req import SteamApiRequest
from .const import APP_ENDPOINT
import requests
from .. import error


def get_app_list():
    return SteamApiRequest.get(
        APP_ENDPOINT,
        '/GetAppList',
        'v2',
    )

def get_app_detail(appid, cc='cn'):
    payload = {
        'appids': appid,
        'cc': cc
    }

    response = requests.get('https://store.steampowered.com/api/appdetails', params=payload)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        error.handle_error(response)
