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

print("\nAVAILABLE STREAMS:")
all_streams(link)
stream_itag = input("\nPlease enter the stream itag: ")

filename = download_yt_video(link, FOLDER, stream_itag)  # run the download function and save the filename
print("\nStream download completed!")
filename_ = filename.split('.')[0]  # filename without extension
download_subtitles(link, f"{FOLDER}/{filename_}")

mp3_ = input("\nDo you want to convert to mp3? (type 'y' convert): ")
if mp3_ == "y":
    mp4_file_path = f"{FOLDER}/{filename}"
    mp3_file_path = f"{FOLDER}/{filename_}.mp3"
    convert_mp4_to_mp3(mp4_file_path, mp3_file_path)
