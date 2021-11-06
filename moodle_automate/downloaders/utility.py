from os import makedirs
from os.path import dirname
from os.path import exists

# pylint: disable=R0903


class Utility:
    """Utility class for downloader classes"""

    @staticmethod
    def destination_exists(dest_path):
        """returns destination directory or base directory path"""
        destination_directory = dirname(dest_path)
        if not exists(destination_directory):
            makedirs(destination_directory)

        return destination_directory
