import os
import shutil
import urllib3
from functools import wraps
from bs4 import BeautifulSoup
from moodle_automate.const import config, preference

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UserChoiceError(Exception):
    """Raised when choice is in wrong range"""

    pass


class UnplayableStream(Exception):
    "Raised when mpv/vlc cannot stream the url"
    pass


class RequestURL:
    """Requests the url and returns the soup."""

    def __init__(self, URL, session, headers) -> None:
        self.URL = URL
        self.session = session
        self.headers = headers

    def __enter__(self) -> "soup":
        self.html = self.session.get(self.URL, verify=False, headers=self.headers)
        self.soup = BeautifulSoup(self.html.text, "html5lib")

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

    def __enter__(self) -> "resp":
        self.responce = self.session.post(
            self.URL, verify=False, headers=self.headers, data=self.payload
        )

        return self.responce

    def __exit__(self, exec_type, exec_value, exec_trace) -> None:
        pass


def check_config(func):
    """checks if the config has username and password defined"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if config["username"] is None or config["password"] is None:
            return "Provide credentials with python gehu.py --username <YOUR_USERNAME> --password <YOUR_PASSWORD> "

        return func(*args, **kwargs)

    return wrapper


def check_preference_video(func):
    """checks if the preference has player and browser defined"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        def cmd_exists(x):
            return shutil.which(x) is not None

        if (
            not cmd_exists(preference["player"])
            or not cmd_exists(preference["browser"])
            or preference["watch_video_resolution"]
            not in ("144", "360", "480", "720", "1080", "1440")
            or preference["download_video_resolution"]
            not in ("144", "360", "480", "720", "1080", "1440")
        ):
            return "Provide preference with python gehu.py --player <YOUR_PREFERRED_MEDIA_PLAYER> --browser <YOUR_PREFERRED_BROWSER> "

        return func(*args, **kwargs)

    return wrapper


def check_preference_download_dir(func):
    """checks if the preference has download directory defined and is valid"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if preference["download_dir"] is None or not os.path.exists(
            preference["download_dir"]
        ):
            return "Provide preference with python gehu.py --download-dir <PATH TO DOWNLOAD DIRECTORY> "

        return func(*args, **kwargs)

    return wrapper
