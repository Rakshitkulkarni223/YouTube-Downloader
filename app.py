from flask import Flask, request, render_template, send_file
from pytube import YouTube
import logging, sys
import instagram
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)

resolutions = ['Auto', '144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2040p']


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
    global resolutions
    try:
        input_url = request.form['URL']

        resolu = set()

        for stream in YouTube(input_url).streams.filter(progressive=True).order_by('resolution'):
            resolu.add(stream.resolution)

        resolu = sorted(list(resolu))

        res = request.form['resolution']

        flag = False

        for resolution in resolu:
            if res == resolution:
                flag = True
                video = YouTube(str(input_url)).streams.filter(progressive=True,resolution=res).first()
                break

        if not flag:
            video = YouTube(str(input_url)).streams.filter(progressive=True,resolution=resolu[len(resolu) - 1]).first()

        name = video.title

        if '|' in name:
            name = name.split('|')[0]

        video.download(filename=name + '.mp4')

        return send_file(f"{name}.mp4", as_attachment=True)
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
            name = name.split('|')[0]

        audio_file.streams.get_audio_only().download(filename=name + '.mp3')

        return send_file(f"{name}.mp3", as_attachment=True)

    except:
        logging.exception('Failed download')
        return 'Audio download failed!'


# Instagram
res=[]

@app.route("/Download_reel")
def Download_reel():
    global res
    try:
        username = "rakshit__kulkarni"
        password = "196219992002@rdks"
        res = instagram.authontication(username, password)
        if res[1].get("authenticated"):
            return render_template("Instagram_reel.html")
        else:
            return render_template('Home.html')
    except:
        return render_template('Home.html')

# @app.route("/Instagram_Download",methods=['GET', 'POST'])
# def Instagram_Download():
#     global res
#     try:
#         username = request.form['username']
#         password = request.form['password']
#         res=instagram.authontication(username,password)
#         if res[1].get("authenticated"):
#             return render_template("Instagram_reel.html")
#         else:
#             return render_template('Instagram_login.html', login_info="Login Failed!!")
#     except:
#         return render_template('Instagram_login.html',login_info="Login Failed!!")

# @app.route("/authorization")
# def authorization():
#     global res
#     try:
#         if res[1].get("authenticated"):
#             return render_template("Instagram_reel.html")
#         else:
#             return render_template('Instagram_login.html')
#     except:
#         return render_template('Instagram_login.html')


@app.route("/Download_post")
def Download_post():
    global res
    try:
        if res[1].get("authenticated"):
            return render_template("Instagram_post.html")
        else:
            username = "rk_utube_insta_download"
            password = "rakshitkulkarni2021"
            res = instagram.authontication(username, password)
            if res[1].get("authenticated"):
                return render_template("Instagram_post.html")
            else:
                return render_template('Home.html')
    except:
        return render_template('Home.html')


@app.route("/download_insta_reel", methods=['GET', 'POST'])
def download_insta_reel():
    try:
        input_url = request.form['URL']

        filename = instagram.Download_reel(input_url,res[0],res[1])

        if filename == "None":
            logging.exception('Failed download')
            return "Instagram Reel download failed!"

        return send_file(f"{filename}.mp4", as_attachment=True)
    except:
        logging.exception('Failed download')
        return "Instagram Reel download failed!"


@app.route("/download_insta_post", methods=['GET', 'POST'])
def download_insta_post():
    try:
        input_url = request.form['URL']

        filename = instagram.Download_Post(input_url,res[0],res[1])

        if filename == "None":
            logging.exception('Failed download')
            return "Instagram Post download failed!"

        return send_file(f"{filename}.jpg", as_attachment=True)
    except:
        logging.exception('Failed download')
        return "Instagram Post download failed!"


if __name__ == '__main__':
    app.run(debug=True)