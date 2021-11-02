from moodle_automate.downloaders.drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(
    file_id="1iytA1n2z4go3uVCwE__vIKouTKyIDjEq",
    dest_path="./data/ex.zip",
    showsize=True,
)
