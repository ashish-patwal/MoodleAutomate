from subprocess import Popen, PIPE
from urllib.parse import urlparse
import urllib3
import os

from context import check_preference_video, check_preference_downloadDir
from const import preference

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@check_preference_video
def play_video(url, session, headers) -> None:
    """Plays the video on media player if it's youtube otherwise on browser."""
    responce = session.get(url, verify=False, headers=headers)

    #load_preference()

    if urlparse(responce.url).netloc.find('drive.google.com') != -1:
        p = Popen([preference['browser'], responce.url], stdout=PIPE, stderr=PIPE)
        #stdout, stderr = p.communicate()

    elif urlparse(responce.url).netloc.find('youtube') != -1:
        p = Popen([preference['player'], responce.url], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        p.wait()
    
    else:
        print('ptanin kahan dali hai video')


@check_preference_downloadDir
def download_resource(url, session, headers) -> None:
    """Downloads the file resource and saves it in current directory."""
    responce = session.get(url, verify=False, headers=headers)

    filename = os.path.join(preference['download_dir'], os.path.basename(urlparse(responce.url).path))

    with open(filename, 'wb') as file:
        file.write(responce.content)
