import os.path

from flask import Flask, request, render_template, send_file
from pytube import YouTube
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('MP4.html')

@app.route("/Download_MP4")
def Download_MP4():
    return render_template('MP4.html')

@app.route("/Download_MP3")
def Download_MP3():
    return render_template('MP3.html')

@app.route('/download_video', methods=['GET', 'POST'])
def download_video():
    try:
        input_url = request.form['URL']
        # print(YouTube(input_url).streams.all())
        video=YouTube(str(input_url)).streams.filter(resolution="720p",file_extension='mp4').first()

        # for stream in YouTube(input_url).streams:
        #     print(stream["res"])
        # video.resolution="720p"
        # print("video: ",video)
        path=video.download()
        # print("path :",path)
        fname = path.split('//')[-1]
        # print(fname)
        return send_file(fname, as_attachment=True)
    except:
        logging.exception('Failed download')
        return 'Video download failed!'

@app.route('/download_audio', methods=['GET', 'POST'])
def download_audio():
    try:
        input_url = request.form['URL']

        audio_file = YouTube(input_url)
        audio = audio_file.streams.get_by_itag("140")  # stream itag 140 is for mp4 audio
        songName = audio_file.title
        audio.download()
        os.rename(songName + ".mp4", songName + ".mp3")
        return send_file(songName+".mp3", as_attachment=True)
    except:
        logging.exception('Failed download')
        return 'Audio download failed!'


if __name__ == "__main__":
    app.run(debug=True)