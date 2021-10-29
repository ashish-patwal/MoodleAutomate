import requests
from subprocess import run, CalledProcessError
from urllib.parse import urlparse
import urllib3
import sys
import os

from context import check_preference_video, check_preference_download_dir, \
    UnplayableStream
from const import preference

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@check_preference_video
def play_video(url, session=None, headers=None) -> None:
    """Plays the video on media player if it's youtube otherwise on browser."""
    if session and headers:
        responce = session.get(url, verify=False, headers=headers)
    else:
        responce = requests.get(url)

    mpv_args = {
        "shuffle": "-shuffle",
        "format": f"--ytdl-format=bestvideo[height<=?\
                {preference['video_resolution']}][fps<=?30]+\
                bestaudio/best[height<={preference['video_resolution']}]",
        "subLang": "--ytdl-raw-options=sub-lang=en,write-auto-sub=,yes-playlist=",
        "window": "--force-window=immediate"
    }

    try:

        if urlparse(responce.url).netloc.find('drive.google.com') != -1:
            run([preference['browser'], responce.url], check=True)

        elif urlparse(responce.url).netloc.find('youtube') != -1:
            run([preference['player'], mpv_args['format'], mpv_args['subLang'],
                mpv_args['window'], responce.url], check=True,
                capture_output=True)

        else:
            process = run([preference['player'], responce.url],
                          check=False, capture_output=False)
            if process.returncode != 0:
                raise UnplayableStream

    except CalledProcessError:
        print('Some Error with process execution')
        sys.exit(1)

    except UnplayableStream:
        print('Stream is unplayable via mpv/vlc on some unknown platform')
        sys.exit(1)


@check_preference_download_dir
def download_resource(url, session, headers) -> None:
    """Downloads the file resource and saves it in current directory."""
    responce = session.get(url, verify=False, headers=headers)
    total = responce.headers.get('content-length')

    filename = os.path.join(
        preference['download_dir'],
        os.path.basename(urlparse(responce.url).path))

    with open(filename, 'wb') as file:

        if total is None:
            file.write(responce.content)

        else:
            downloaded = 0
            total = int(total)
            print('Downloading ... ')
            for data in responce.iter_content(chunk_size=max(int(total/1000),
                                                             1024*1024)):
                downloaded += len(data)
                file.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format(
                    '█' * done, '.' * (50 - done)))
                sys.stdout.flush()

    sys.stdout.write('\n')
