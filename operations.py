import requests
from subprocess import Popen, PIPE
from urllib.parse import urlparse
import urllib3
import sys
import os

from context import check_preference_video, check_preference_downloadDir
from const import preference

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@check_preference_video
def play_video(url, session=None, headers=None) -> None:
    """Plays the video on media player if it's youtube otherwise on browser."""
    if session and headers:
        responce = session.get(url, verify=False, headers=headers)
    else:
        responce = requests.get(url)

    # load_preference()

    if urlparse(responce.url).netloc.find('drive.google.com') != -1:
        p = Popen([preference['browser'], responce.url],
                  stdout=PIPE, stderr=PIPE)
        # stdout, stderr = p.communicate()

    elif urlparse(responce.url).netloc.find('youtube') != -1:
        p = Popen([preference['player'], responce.url],
                  stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        p.wait()

    else:
        print('Unknown platform used')


@check_preference_downloadDir
def download_resource(url, session, headers) -> None:
    """Downloads the file resource and saves it in current directory."""
    responce = session.get(url, verify=False, headers=headers)
    total = responce.headers.get('content-length')

    filename = os.path.join(
        preference['download_dir'], os.path.basename(urlparse(responce.url).path))

    with open(filename, 'wb') as file:

        if total is None:
            file.write(responce.content)

        else:
            downloaded = 0
            total = int(total)
            print('Downloading ... ')
            for data in responce.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                file.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format(
                    '█' * done, '.' * (50 - done)))
                sys.stdout.flush()

    sys.stdout.write('\n')
