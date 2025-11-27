from functions import *
from pytubefix.exceptions import RegexMatchError

FOLDER = "download"  # path to the folder where you want to download the files


while True:
    link = input("Please enter the link of the Youtube video: ")
    try:
        YouTube(link)  # check if the url is a valid YouTube url
        break
    except RegexMatchError:
        print("You entered an invalid url. Check the url and try again!\n")

streams = input("\nPress ENTER to download the best quality stream available (720p max),\n"
                "or type 's' if you want to see a list of all available video streams: ")

if streams == "s":
    print("\nList of all streams:")
    all_streams(link)
    stream_itag = input("\nPlease enter the stream itag: ")
else:
    stream_itag = None

filename = download_yt_video(link, FOLDER, stream_itag)  # run the download function and save the filename
filename_ = filename.split('.')[0]  # filename without extension
download_subtitles(link, f"{FOLDER}/{filename_}")

mp3_ = input("\nDo you want to convert to mp3? (type 'y' convert): ")
if mp3_ == "y":
    mp4_file_path = f"{FOLDER}/{filename}"
    mp3_file_path = f"{FOLDER}/{filename_}.mp3"
    convert_mp4_to_mp3(mp4_file_path, mp3_file_path)
