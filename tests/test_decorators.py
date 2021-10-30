import unittest
from moodle_automate.context import check_config, check_preference_video, \
    check_preference_download_dir
from moodle_automate.parser import load_config, load_preference
from moodle_automate.const import config, preference


class TestsDecorators(unittest.TestCase):
    """class to test function decorators"""

    def setUp(self):
        """set up"""

        self.test_func = lambda: True

    def test_config_not_exists(self):
        """tests results if config does not exists"""

        test_config = {"logintoken": None, "username": None, "password": None}
        config.update(test_config)

        res = check_config(self.test_func)
        self.assertIsInstance(res(), str)

    def test_config_exists(self):
        """tests results if config exists"""

        load_config()

        res = check_config(self.test_func)
        self.assertTrue(res())

    def test_preference_video_not_exists(self):
        """tests results if preference for video players and browsers are not
        defined / exists in system path and video resolution is not correct"""

        res = check_preference_video(self.test_func)

        test_false_player_preference = {
            "player": 'false_player', "browser": 'chrome', "video_resolution": '720'}
        preference.update(test_false_player_preference)
        self.assertIsInstance(res(), str)

        test_false_browser_preference = {
            "player": 'mpv', "browser": 'false_browser', "video_resolution": '720'}
        preference.update(test_false_browser_preference)
        self.assertIsInstance(res(), str)

        test_false_resolution_preference = {
            "player": 'mpv', "browser": 'brave', "video_resolution": '999'}
        preference.update(test_false_resolution_preference)
        self.assertIsInstance(res(), str)

    def test_preference_video_exists(self):
        """tests results if preference for video players / browsers / video resolution are correct"""

        load_preference()

        res = check_preference_video(self.test_func)
        self.assertTrue(res())

    def test_preference_download_dir_not_exists(self):
        """tests results if preference for download dir doesn't exist or is an invalid path"""

        res = check_preference_download_dir(self.test_func)

        test_empty_path_preference = {
            "download_dir": None}
        preference.update(test_empty_path_preference)
        self.assertIsInstance(res(), str)

        test_invalid_path_preference = {
            "download_dir": '/home/dummy/false_dir/'}
        preference.update(test_invalid_path_preference)
        self.assertIsInstance(res(), str)

    def test_preference_download_dir_exists(self):
        """tests results if preference for download dir exists and is a valid path"""

        test_valid_path_preference = {"download_dir": '/home/lucifer/.moodle/'}
        preference.update(test_valid_path_preference)

        res = check_preference_download_dir(self.test_func)
        self.assertTrue(res())
