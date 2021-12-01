from flask import Flask, request, render_template, send_file
from pytube import YouTube
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('YouTube.html')


@app.route('/download_video', methods=['GET', 'POST'])
def download_video():
    try:
        input_url = request.form['URL']
        # print(YouTube(input_url).streams.all())
        video=YouTube(input_url).streams.filter(resolution="720p",file_extension='mp4').first()

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


if __name__ == "__main__":
    app.run(debug=True)