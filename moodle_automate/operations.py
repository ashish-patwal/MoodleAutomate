import os
import sys
import urllib3
import requests
from urllib.parse import urlparse
from subprocess import run, CalledProcessError

from moodle_automate.const import preference
from moodle_automate.downloaders.drive_downloader import GoogleDriveDownloader as GDD
from moodle_automate.context import (
    UnplayableStream,
    check_preference_video,
    check_preference_download_dir,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@check_preference_video
def play_video(url, session=None, headers=None) -> None:
    """Plays the video on media player if it's youtube otherwise on browser."""
    # TODO: Remove this logic of parsing session and headers for show_motive .
    if session and headers:
        responce = session.get(url, verify=False, headers=headers)
    else:
        responce = requests.get(url)

    mpv_args = {
        "shuffle": "-shuffle",
        "format": f"--ytdl-format=bestvideo[height<=?{preference['watch_video_resolution']}][fps<=?30]+bestaudio/best[height<={preference['watch_video_resolution']}]",
        "subLang": "--ytdl-raw-options=sub-lang=en,write-auto-sub=,yes-playlist=",
        "window": "--force-window=immediate",
    }

    try:

        if urlparse(responce.url).netloc.find("drive.google.com") != -1:
            sess = requests.Session()

            file_title = GDD.get_file_title(responce.url)

            if not file_title.endswith((".mp4", ".mkv", ".webm")):
                raise UnplayableStream

            file_id = GDD.get_file_id(responce.url)
            drive_video = sess.get(
                GDD.DOWNLOAD_URL, params={"id": file_id}, stream=True
            )

            token = GDD.get_confirm_token(drive_video)
            if token:
                params = {"id": file_id, "confirm": token}
                drive_video = sess.get(GDD.DOWNLOAD_URL, params=params, stream=True)

            run(
                [
                    preference["player"],
                    mpv_args["format"],
                    mpv_args["subLang"],
                    mpv_args["window"],
                    drive_video.url,
                ],
                check=True,
                capture_output=True,
            )

        elif urlparse(responce.url).netloc.find("youtube") != -1:
            run(
                [
                    preference["player"],
                    mpv_args["format"],
                    mpv_args["subLang"],
                    mpv_args["window"],
                    responce.url,
                ],
                check=True,
                capture_output=True,
            )

        else:
            process = run(
                [preference["player"], responce.url], check=False, capture_output=False
            )
            if process.returncode != 0:
                raise UnplayableStream

    except CalledProcessError:
        print("Some Error with process execution")
        sys.exit(1)

    except UnplayableStream:
        print("Stream is unplayable via mpv/vlc on some unknown platform")
        sys.exit(1)


@check_preference_download_dir
def download_resource(url, session, headers, subject_title) -> None:
    """Downloads the file resource and saves it in current directory."""

    if not os.path.exists(preference["download_dir"]):
        os.mkdir(preference["download_dir"])

    subject_directory = os.path.join(preference["download_dir"], subject_title)

    if not os.path.exists(subject_directory):
        os.mkdir(subject_directory)

    responce = session.get(url, verify=False, headers=headers)
    total = responce.headers.get("content-length")

    filename = os.path.join(
        subject_directory, os.path.basename(urlparse(responce.url).path)
    )

    if os.path.exists(filename):
        input("[download] {} already exists . Enter to continue .".format(filename))
        return

    current_download_size = [0]
    print("[download] Destination: {}".format(filename))
    sys.stdout.flush()

    GDD.save_response_content(responce, filename, True, current_download_size)


# TODO: cleanup
#    with open(filename, "wb") as file:

#        if total is None:
#            file.write(responce.content)

#        else:
#            downloaded = 0
#            total = int(total)
#            print("Downloading ... ")
#            for data in responce.iter_content(
#                chunk_size=max(int(total / 1000), 1024 * 1024)
#            ):
#                downloaded += len(data)
#                file.write(data)
#                done = int(50 * downloaded / total)
#                sys.stdout.write("\r[{}{}]".format("█" * done, "." * (50 - done)))
#                sys.stdout.flush()

#    sys.stdout.write("\n")
