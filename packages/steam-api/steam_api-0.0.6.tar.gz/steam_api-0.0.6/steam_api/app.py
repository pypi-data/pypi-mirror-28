from .api.app import get_app_list, get_app_detail


class App(object):
    """
    Steam App Service
    """

    def __init__(self):
        pass

    @staticmethod
    def list():
        """
        Gets the complete list of public apps.

        Sample

        .. code-block:: javascript

            [{
                "appid": 5,
                "name": "Dedicated Server"
            },
            {
                "appid": 7,
                "name": "Steam Client"
            },
            {
                "appid": 8,
                "name": "winui2"
            }]

        :return: list(dict)
        """
        res = get_app_list()
        app_list = res['applist']

        return app_list['apps']

    @staticmethod
    def detail(id):
        """
        Get the detail of an app with id and locale

        Sample

        .. code-block:: javascript
    
            {
                "type": "game",
                "name": "xxxxx",
                "steam_appid": 192929
                ...
            }
    
        :retutn: dict
        """
        res = get_app_detail(id)
        data = res[str(id)]
        return data['data']
