from const import config, preference

from bs4 import BeautifulSoup
from functools import wraps
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class userChoiceError(Exception):
    """Raised when choice is in wrong range"""
    pass


class RequestURL:
    """Requests the url and returns the soup."""

    def __init__(self, URL, session, headers) -> None:
        self.URL = URL
        self.session = session
        self.headers = headers

    def __enter__(self) -> 'soup':
        self.html = self.session.get(
            self.URL, verify=False, headers=self.headers)
        self.soup = BeautifulSoup(self.html.text, 'html5lib')

        return self.soup

    def __exit__(self, exec_type, exec_value, exec_trace) -> None:
        pass


class PostToURL:
    """Post requests to the url and returns the responce."""

    def __init__(self, URL, session, headers, payload) -> None:
        self.URL = URL
        self.session = session
        self.headers = headers
        self.payload = payload

    def __enter__(self) -> 'resp':
        self.responce = self.session.post(
            self.URL, verify=False, headers=self.headers, data=self.payload)

        return self.responce

    def __exit__(self, exec_type, exec_value, exec_trace) -> None:
        pass


def check_config(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not config['username'] or not config['password']:
            print(
                'Provide credentials with python gehu.py --username <YOUR_USERNAME> --password <YOUR_PASSWORD> ')
        else:
            return(func(*args, **kwargs))

    return wrapper


def check_preference_video(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not preference['player'] or not preference['browser']:
            print('Provide preference with python gehu.py --player <YOUR_PREFERRED_MEDIA_PLAYER> --browser <YOUR_PREFERRED_BROWSER> ')
        else:
            return(func(*args, **kwargs))

    return wrapper


def check_preference_downloadDir(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not preference['download_dir']:
            print(
                'Provide preference with python gehu.py --download-dir <PATH TO DOWNLOAD DIRECTORY> ')
        else:
            return(func(*args, **kwargs))

    return wrapper
