from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip
from pytubefix.exceptions import RegexMatchError
import pysrt

FOLDER = "download"  # path to the folder where you want to download the files
yt = None  # YouTube object


def get_yt():
    global yt
    while True:
        link = input("Please enter the link of the Youtube video: ")
        try:
            yt = YouTube(link, on_progress_callback=on_progress)
            print()
            print(yt.title)  # check if the url is a valid YouTube url and print the title
            print(f"by: {yt.author}")
            print(15 * "-")
            print(yt.video_id)
            # print(yt.__dict__.keys())
            break
        except RegexMatchError:
            print("You entered an invalid url. Check the url and try again!\n")


def all_streams():
    global yt
    # stream = yt.streams.filter(only_video=True)  # only video (without audio) streams
    # stream = yt.streams.filter(only_audio=True)  # only audio streams
    # stream = yt.streams.filter(progressive=True)  # only videos with audio streams
    # stream = yt.streams.all()  # all streams
    streams = yt.streams  # all streams

    print("AVAILABLE STREAMS:")
    for stream in streams:
        # print(stream)
        #  change video/mp4, video/webm, audio/mp4 and audio/webm to mp4 or webm
        if "mp4" in stream.mime_type:
            stream.mime_type = "mp4 "
        else:
            stream.mime_type = "webm"

        if stream.type == "audio":
            stream.fps = "-"
            stream.type = "audio only "
            stream.resolution = "---"
        else:
            if stream.is_progressive:
                stream.type = "video+audio"
            else:
                stream.type = "video only "

        print(f"itag: {stream.itag} \t {stream.type} - {stream.mime_type} \t fps: {stream.fps} \t "
              f"resolution: {stream.resolution} \t filesize: {stream.filesize / 1048576:.1f} MB")

    print(15 * "-")
    video_p = streams.get_highest_resolution()
    print(f"Highest resolution with audio - itag: {video_p.itag}")


def download_yt_video():
    global yt

    itag = input("\nPlease enter the stream itag: ")

    if itag:
        video = yt.streams.get_by_itag(itag, )
        if video:  # if itag exists
            print(f"\nDownloading video itag {itag}:")
        else:  # if itag is wrong, no video
            print("\nWrong itag, downloading highest resolution with audio:")
            video = yt.streams.get_highest_resolution()
    else:
        print("\nNo itag, downloading highest resolution with audio:")
        video = yt.streams.get_highest_resolution()
    print(video.title)
    video.download(FOLDER)
    print("Download completed!")
    return video.default_filename  # returns the filename


def convert_mp4_to_mp3(mp4_in, mp3_out):
    try:
        mp4 = VideoFileClip(mp4_in)
        mp3 = mp4.audio
        try:
            mp3.write_audiofile(mp3_out)
            mp3.close()
        except AttributeError:
            print("Sorry, no audio in this file, try another stream with audio.")
        mp4.close()

    except OSError:
        print("Sorry, video file does not exist, please try another stream.")


def download_subtitles(file_path="captions"):
    global yt
    all_captions = yt.captions

    if "en" in all_captions:
        captions = yt.captions["en"]
    elif "a.en" in all_captions:
        captions = yt.captions["a.en"]
    else:
        captions = None
        print("Sorry, no english subtitles in this video.")

    if captions:
        # # save to txt file
        # captions.save_captions(f"{file_path}.txt")

        # save to srt file
        srt_captions = captions.generate_srt_captions()
        with open(f"{file_path}.srt", "w") as srt_file:
            srt_file.writelines(srt_captions)

        # convert srt to txt
        subs = pysrt.open(f"{file_path}.srt", encoding='unicode_escape')
        txt_captions = ""
        for sub in subs:
            txt_captions += f"{sub.text}\n\n"
        with open(f"{file_path}.txt", "w") as txt_file:
            txt_file.writelines(txt_captions)

        print("Subtitles download completed!")
