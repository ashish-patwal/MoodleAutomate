from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
