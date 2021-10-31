import unittest
import requests
import urllib3
from moodle_automate.const import URL, MAINURL, config, headers
from moodle_automate.context import RequestURL, PostToURL
from moodle_automate.parser import load_config


class TestContextManager(unittest.TestCase):
    """class to test context managers"""

    def test_login(self):
        """tests login with RequestURL and PostToURL"""

        load_config()

        with requests.Session() as session:
            with RequestURL(URL, session, headers) as soup:
                config['logintoken'] = soup.find(
                    'input', {'name': 'logintoken'})['value']

            with PostToURL(URL, session, headers, config) as response:
                self.assertEqual(response.url, MAINURL)

    def test_requesturl(self):
        """tests RequestURL context manager"""

        with requests.Session() as session:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning)
            with RequestURL('https://en.wikipedia.org/wiki/Netscape_Navigator',
                            session, headers) as soup:
                response = soup.find(
                    "meta", attrs={"property": "og:image"}).attrs["content"]

        self.assertEqual(
            response, 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netscape_icon.svg/1200px-Netscape_icon.svg.png')

    def test_posttourl(self):
        """tests PostToURL context manager"""

        test_config = {
            "logintoken": "false_token",
            "username": "false_usernmae",
            "password": "false_password"
        }

        with requests.Session() as session:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning)
            with PostToURL(URL, session, headers, test_config) as response:
                # allow-redirection overwrites the response codes . Therefore need to compare results with redirected url .
                self.assertNotEqual(response.url, MAINURL)
