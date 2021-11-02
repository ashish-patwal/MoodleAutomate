import requests
import zipfile
import warnings
from sys import stdout
from os.path import exists
from moodle_automate.downloaders.utility import Utility


class GoogleDriveDownloader(Utility):
    """
    Minimal class to download shared files from Google Drive.
    """

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

    @staticmethod
    def download_file_from_google_drive(
        file_id, dest_path, overwrite=False, showsize=True
    ):
        """
        Downloads a shared file from google drive into a given folder.
        """

        destination_directory = Utility.destination_exists(dest_path)

        if not exists(dest_path) or overwrite:

            session = requests.Session()

            print("[download] Destination: {}".format(dest_path), end="")
            stdout.flush()

            response = session.get(
                GoogleDriveDownloader.DOWNLOAD_URL, params={"id": file_id}, stream=True
            )

            token = GoogleDriveDownloader._get_confirm_token(response)
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
            # print("Done.")

    #            if unzip:
    #                try:
    #                    print("Unzipping...", end="")
    #                    stdout.flush()
    #                    with zipfile.ZipFile(dest_path, "r") as z:
    #                        z.extractall(destination_directory)
    #                    print("Done.")
    #                except zipfile.BadZipfile:
    #                    warnings.warn(
    #                        'Ignoring `unzip` since "{}" does not look like a valid zip file'.format(
    #                            file_id
    #                        )
    #                    )

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    @staticmethod
    def _save_response_content(response, destination, showsize, current_size):
        with open(destination, "wb") as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    if showsize:
                        print(
                            "\r[download] "
                            + GoogleDriveDownloader.sizeof_fmt(current_size[0]),
                            end=" ",
                        )
                        stdout.flush()
                        current_size[0] += GoogleDriveDownloader.CHUNK_SIZE

    # From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "{:.1f} {}{}".format(num, unit, suffix)
            num /= 1024.0
        return "{:.1f} {}{}".format(num, "Yi", suffix)
