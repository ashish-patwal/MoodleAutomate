import random
import string
import unittest
from moodle_automate.downloaders.utility import Utility
from moodle_automate.downloaders.drive_downloader import GoogleDriveDownloader as GDD
from moodle_automate.downloaders.youtube_downloader import YoutubeDownloader as YD


class TestDownloaders(unittest.TestCase):
    """class to tests downloader classes"""

    def setUp(self) -> None:
        self.dest_path_list = {
            "/home/lucifer": "/home/lucifer/Desktop",
            "/home/lucifer/.moodle": "/home/lucifer/.moodle/downloads",
            "/home/lucifer/Desktop": "/home/lucifer/Desktop/test",
            "/home/lucifer/Desktop/test": "/home/lucifer/Desktop/test/aria",
        }

    def test_Utility(self):
        utility_instance = Utility()
        for key, value in self.dest_path_list.items():
            self.assertEqual(key, utility_instance.destination_exists(value))

    def test_GDD_save_file_path(self):
        gdd_instance = GDD()
        file_id = {}
        for _ in range(10):
            rand_str = "".join(
                random.choices(string.ascii_letters + string.digits, k=16)
            )
            file_id.update(
                {f"https://drive.google.com/file/d/{rand_str}/view": rand_str}
            )

        for key, value in file_id.items():
            self.assertEqual(value, gdd_instance.get_file_id(key))
