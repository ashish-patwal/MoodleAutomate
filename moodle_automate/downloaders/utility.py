from os import makedirs
from os.path import dirname
from os.path import exists


class Utility:
    """Utility class for downloader classes"""

    @staticmethod
    def destination_exists(dest_path):
        destination_directory = dirname(dest_path)
        if not exists(destination_directory):
            makedirs(destination_directory)

        return destination_directory
