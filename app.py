import os.path

from flask import Flask, request, render_template, send_file
from pytube import YouTube
import logging
import sys
from moviepy.editor import *

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
        video = YouTube(str(input_url)).streams.filter(resolution="720p", file_extension='mp4').first()
        path = video.download()
        fname = path.split('//')[-1]
        return send_file(fname, as_attachment=True)
    except:
        logging.exception('Failed download')
        return 'Video download failed!'


@app.route('/download_audio', methods=['GET', 'POST'])
def download_audio():
    try:
        input_url = request.form['URL']

        audio=YouTube(input_url)

        file=audio.streams.filter(only_audio=True).first().download()

        return send_file(file, as_attachment=True)
    except:
        logging.exception('Failed download')
        return 'Audio download failed!'


if __name__ == "__main__":
    app.run(debug=True)
