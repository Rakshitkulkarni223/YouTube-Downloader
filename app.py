from flask import Flask, request, render_template, send_file
from pytube import YouTube
import logging,sys
import instagram

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)

resolutions=['Auto','144p','240p','360p','480p','720p','1080p','1440p','2040p']

@app.route("/")
def home():
    return render_template('Home.html')

# YouTube

@app.route("/Download_MP4")
def Download_MP4():
    global resolutions
    return render_template('MP4.html', resolutions=resolutions)


@app.route("/Download_MP3")
def Download_MP3():
    return render_template('MP3.html')


@app.route('/download_video', methods=['GET', 'POST'])
def download_video():
    try:
        global filesize
        input_url = request.form['URL']

        resolu = set()

        for stream in YouTube(input_url).streams.filter(progressive=True).order_by('resolution'):
            resolu.add(stream.resolution)

        resolu=sorted(list(resolu))

        res=request.form['resolution']

        flag=False

        for resolution in resolu:
            if res==resolution:
                flag=True
                video = YouTube(str(input_url)).streams.filter(progressive=True, resolution=resolution, file_extension='mp4').first()
                break

        if not flag:
            video = YouTube(str(input_url)).streams.filter(progressive=True, resolution=resolu[len(resolu)-1],
                                                           file_extension='mp4').first()


        name = video.title

        # filesize=video.filesize

        # print(filesize)
        #
        # check()

        if '|' in name:
            name=name.split('|')[0]

        video.download(output_path='download', filename=name + '.mp4')

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

        if '|' in name:
            name=name.split('|')[0]

        audio_file.streams.get_audio_only().download(output_path='download', filename=name + '.mp3')

        return send_file(f"download/{name}.mp3",as_attachment=True)
    
    except:
        logging.exception('Failed download')
        return 'Audio download failed!'


# Instagram

@app.route("/Download_reel")
def Download_reel():
    return render_template('Instagram_reel.html')


@app.route("/Download_post")
def Download_post():
    return render_template('Instagram_post.html')

@app.route("/download_insta_reel", methods=['GET', 'POST'])
def download_insta_reel():
    try:
        input_url = request.form['URL']
        username = "rakshit__kulkarni"
        password = "196219992002@rdks"
        filename=instagram.Download_reel(input_url,username,password)

        if filename=="None":
            logging.exception('Failed download')
            return 'Instagram Reel download failed!'

        return send_file(f"download\\{filename}.mp4", as_attachment=True)
    except:
        logging.exception('Failed download')
        return 'Instagram Reel download failed!'


if __name__ == '__main__':
    # filesize=0
    app.run(debug=True)