from functions import *


get_yt()

all_streams()

filename = download_yt_video()  # run the download function and save the filename
print(filename)
filename_ = filename.split('.')[0]  # filename without extension

download_subtitles(f"{FOLDER}/{filename_}")

mp3_ = input("\nDo you want to convert to mp3? (type 'y' convert): ")
if mp3_ == "y":
    mp4_file_path = f"{FOLDER}/{filename}"
    mp3_file_path = f"{FOLDER}/{filename_}.mp3"
    convert_mp4_to_mp3(mp4_file_path, mp3_file_path)
