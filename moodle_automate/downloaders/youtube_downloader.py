import sys
import subprocess
from os.path import exists
from moodle_automate.downloaders.utility import Utility
from moodle_automate.const import preference


class YoutubeDownloader(Utility):
    """
    Minimal class to download shared files from Youtube .
    """

    CMD = "youtube-dl"
    CMD_ARGS = [
        "-f",
        f"bestvideo[height<={preference['download_video_resolution']}]+bestaudio/best[height<={preference['download_video_resolution']}]",
    ]

    @staticmethod
    def download_file_from_youtube(youtube_url, dest_path):
        """
        Downloads a video file from youtube to a given folder.
        """

        destination_directory = Utility.destination_exists(dest_path)

        if exists(destination_directory):
            print("starting process")
            p = subprocess.Popen(
                [
                    YoutubeDownloader.CMD,
                    *YoutubeDownloader.CMD_ARGS,
                    f"{youtube_url}",
                    "-o",
                    f"{destination_directory}/%(title)s.%(ext)s",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            for line in iter(p.stdout.readline, b""):
                sys.stdout.buffer.write(line)
                sys.stdout.flush()

            return_code = p.wait()

            if return_code:
                print("Something went wrong")
                sys.exit(1)
