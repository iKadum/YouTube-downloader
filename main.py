from functions import *


get_yt()

all_streams()

filename = download_yt_video()  # function returns filename

download_subtitles(filename)

convert_mp4_to_mp3(filename)
