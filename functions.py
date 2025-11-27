from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip
import pysrt


def all_streams(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    # stream = yt.streams.filter(only_video=True)  # only video (without audio) streams
    # stream = yt.streams.filter(only_audio=True)  # only audio streams
    # stream = yt.streams.filter(progressive=True)  # only videos with audio streams
    # stream = yt.streams.all()  # all streams
    stream = yt.streams  # all streams

    for i in stream:
        print(i)


def download_yt_video(url, download_folder=None, itag=None):
    yt = YouTube(url, on_progress_callback=on_progress)
    if itag:
        video = yt.streams.get_by_itag(itag, )
    else:
        video = yt.streams.get_highest_resolution()
    print(f"\nDownloading '{yt.title}' ...")
    video.download(download_folder)
    print("Stream download completed!")
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


def download_subtitles(url, file_path="captions"):
    yt = YouTube(url)
    all_captions = yt.captions

    if "en" in all_captions:
        captions = yt.captions["en"]
    elif "a.en" in all_captions:
        captions = yt.captions["a.en"]
    else:
        captions = None
        print("Sorry, no english subtitles in this video.")
    # to fix the KeyError : 'start', please read this:
    # https://stackoverflow.com/questions/68780808/xml-to-srt-conversion-not-working-after-installing-pytube

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
