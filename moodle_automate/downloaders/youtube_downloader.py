import sys
import subprocess
from os.path import exists
from moodle_automate.downloaders.utility import Utility
from moodle_automate.const import preference

# pylint: disable=R0903


class YoutubeDownloader(Utility):
    """
    Minimal class to download shared files from Youtube .
    """

    CMD = "youtube-dl"

    @staticmethod
    def download_file_from_youtube(youtube_url, destination_directory):
        """
        Downloads a video file from youtube to a given folder.
        """

        cmd_args = [
            "-f",
            f"bestvideo[best[height<={preference['download_video_resolution']}]/height<={preference['download_video_resolution']}]+bestaudio",
        ]

        if exists(destination_directory):
            # pylint: disable=R1732
            video_player_process = subprocess.Popen(
                [
                    YoutubeDownloader.CMD,
                    *cmd_args,
                    f"{youtube_url}",
                    "-o",
                    f"{destination_directory}/%(title)s.%(ext)s",
                ],
            )

            stdout = video_player_process.communicate()

            # TODO: Consider alternatives to reduce bottlenecks in stdout buffers (p.communicate())

            #            for line in iter(p.stdout.readline, b""):
            #                sys.stdout.buffer.write(line)
            #                sys.stdout.flush()

            return_code = video_player_process.wait()

            if return_code:
                print("Something went wrong")
                sys.exit(1)

        else:
            print("directory doesn't exist")
