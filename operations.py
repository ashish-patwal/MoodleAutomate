from subprocess import Popen, PIPE
from urllib.parse import urlparse
import urllib3
import os

from context import check_preference

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@check_preference
def play_video(player, url, session, headers) -> None:
    """Plays the video on media player if it's youtube otherwise on browser."""
    responce = session.get(url, verify=False, headers=headers)

    if urlparse(responce.url).netloc.find('drive.google.com') != -1:
        p = Popen(['brave', responce.url], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

    elif urlparse(responce.url).netloc.find('youtube' != -1):
        p = Popen([player, responce.url], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        p.wait()
    
    else:
        print('ptanin kahan dali hai video')


def download_resource(url, session, headers) -> None:
    """Downloads the file resource and saves it in current directory."""
    responce = session.get(url, verify=False, headers=headers)

    filename = os.path.basename(urlparse(responce.url).path)

    with open(filename, 'wb') as file:
        file.write(responce.content)

