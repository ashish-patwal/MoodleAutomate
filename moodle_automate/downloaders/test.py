from moodle_automate.downloaders.youtube_downloader import YoutubeDownloader

File_Id_1 = "https://www.youtube.com/watch?v=jqKf8ZP-oag"
# File_Id_2 = "https://www.youtube.com/watch?v=jRFIOZuO6Fk"
Dest_Path = "/home/lucifer/Desktop/test/aria/"

YoutubeDownloader.download_file_from_youtube(File_Id_1, Dest_Path)
# YoutubeDownloader.download_file_from_youtube(File_Id_2, Dest_Path)
