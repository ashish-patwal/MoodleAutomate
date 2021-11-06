import sys
import requests
from re import search, error
from os.path import exists, join
from urllib.parse import urlparse

from moodle_automate.downloaders.utility import Utility
from moodle_automate.context import RequestURL, ZeroRegexResultsError


class GoogleDriveDownloader(Utility):
    """
    Minimal class to download shared files from Google Drive.
    """

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

    @staticmethod
    def download_file_from_google_drive(URL, dest_path, overwrite=False, showsize=True):
        """
        Downloads a shared file from google drive into a given folder.
        """

        try:
            file_id = GoogleDriveDownloader.get_file_id(URL)
            file_title = GoogleDriveDownloader.get_file_title(URL)
            dest_path = join(dest_path, file_title)
        except (error, ZeroRegexResultsError):
            print("Regex Error !!")
            sys.exit(1)
        except:
            sys.exit(1)

        if not exists(dest_path) or overwrite:

            session = requests.Session()

            print("[download] Destination: {}".format(dest_path), end="")
            sys.stdout.flush()

            response = session.get(
                GoogleDriveDownloader.DOWNLOAD_URL, params={"id": file_id}, stream=True
            )

            token = GoogleDriveDownloader.get_confirm_token(response)
            if token:
                params = {"id": file_id, "confirm": token}
                response = session.get(
                    GoogleDriveDownloader.DOWNLOAD_URL, params=params, stream=True
                )

            if showsize:
                print()  # Skip to the next line

            current_download_size = [0]
            GoogleDriveDownloader._save_response_content(
                response, dest_path, showsize, current_download_size
            )
            print()

        elif exists(dest_path):
            print(
                "[download] Destination: {} already exists and merged".format(dest_path)
            )
            sys.stdout.flush()

    @staticmethod
    def get_file_id(url):
        """Returns the file_id from google drive link"""
        match = search(r"^/file/d/(.+)/view$", urlparse(url).path)
        if match is not None:
            return match.group(1)
        raise ZeroRegexResultsError

    @staticmethod
    def get_file_title(url):
        """Returns the file_title from google drive link"""
        with RequestURL(url=url) as soup:
            file_title = soup.find("meta", attrs={"property": "og:title"}).attrs[
                "content"
            ]

            return file_title

    @staticmethod
    def get_confirm_token(response):
        """Returns the token when file size is large and google drive asks for confirmation consent"""
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    @staticmethod
    def _save_response_content(response, destination, showsize, current_size):
        with open(destination, "wb") as file:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
                    if showsize:
                        print(
                            "\r[download] "
                            + GoogleDriveDownloader.sizeof_fmt(current_size[0]),
                            end=" ",
                        )
                        sys.stdout.flush()
                        current_size[0] += GoogleDriveDownloader.CHUNK_SIZE

    # From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        """Returns the size of current file size in human readable format"""
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "{:.1f} {}{}".format(num, unit, suffix)
            num /= 1024.0
        return "{:.1f} {}{}".format(num, "Yi", suffix)
