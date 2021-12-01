from flask import Flask, request, render_template, send_file
from pytube import YouTube
import logging,sys

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
        
        name = video.title
        
        video.download(output_path='download/', filename=name + '.mp4')
        
        return send_file(f"download/{name}.mp4",as_attachment=True)
    except:
        logging.exception('Failed download')
        return 'Video download failed!'



@app.route('/download_audio', methods=['GET', 'POST'])
def download_audio():
    try:
        input_url = request.form['URL']

        audio_file = YouTube(input_url)

        name = audio_file.streams.get_audio_only().title

        audio_file.streams.get_audio_only().download(output_path='download/', filename=name + '.mp3')

        return send_file(f"download/{name}.mp3",as_attachment=True)
    
    except:
        logging.exception('Failed download')
        return 'Audio download failed!'


if __name__ == '__main__':
    app.run(debug=True)