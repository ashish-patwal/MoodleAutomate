from bs4 import BeautifulSoup

class RequestURL:

    def __init__(self, URL, session, headers) -> None:
        self.URL = URL
        self.session = session
        self.headers = headers

    def __enter__(self) -> 'soup':
        self.html = self.session.get(self.URL, verify=False, headers=self.headers)
        self.soup = BeautifulSoup(self.html.text, 'html5lib')

        return self.soup

    def __exit__(self, exec_type, exec_value, exec_trace) -> None:
        pass



