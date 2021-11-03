from os import makedirs
from sys import stdout
from os.path import exists, join
from urllib.parse import urlparse
from moodle_automate.const import preference
from moodle_automate.downloaders.drive_downloader import GoogleDriveDownloader as GDD
from moodle_automate.downloaders.youtube_downloader import YoutubeDownloader as YD


class ExternalDownloader(GDD, YD):
    """Main downloader to parse links and download videos into corrosponding directories"""

    # TODO: Remove piping stdout and stderr as using buffers is causing bottlenecks

    def __init__(self, subject_directory):
        self.abs_path = join(preference["video_download_dir"], subject_directory)

        if not exists(self.abs_path):
            makedirs(self.abs_path)

    def download_video(self, URL):
        """Main function to download videos"""

        if urlparse(URL).netloc.find("drive.google.com") != -1:
            print("downloading {}".format(URL))

        elif urlparse(URL).netloc.find("youtube") != -1:
            YD.download_file_from_youtube(URL, self.abs_path)

        else:
            print("some unknown url")
            stdout.flush()
