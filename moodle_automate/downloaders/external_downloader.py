from sys import stdout
from os import makedirs
from os.path import exists, join
from urllib.parse import urlparse
from moodle_automate.const import preference
from moodle_automate.downloaders.youtube_downloader import YoutubeDownloader as YD
from moodle_automate.downloaders.drive_downloader import GoogleDriveDownloader as GDD

# pylint: disable=R0903


class ExternalDownloader(GDD, YD):
    """Main downloader to parse links and download videos into corrosponding directories"""

    # TODO: Remove piping stdout and stderr as using buffers is causing bottlenecks

    def __init__(self, subject_directory):
        self.abs_path = join(preference["video_download_dir"], subject_directory)

        if not exists(self.abs_path):
            makedirs(self.abs_path)

    def download_video(self, url):
        """Main function to download videos"""

        if urlparse(url).netloc.find("drive.google.com") != -1:
            GDD.download_file_from_google_drive(url, self.abs_path)

        elif urlparse(url).netloc.find("youtube") != -1:
            YD.download_file_from_youtube(url, self.abs_path)

        else:
            print("Some unknown url...")
            stdout.flush()
