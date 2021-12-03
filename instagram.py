import json
from datetime import datetime
import requests
from instascrape import Reel

login_response={}
json_data={}

def authontication(username,password):
    global login_response, json_data

    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.now().timestamp())
    response = requests.get(link)
    csrf = response.cookies['csrftoken']

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)

    return login_response,json_data

def Download_reel(url,username,password):
    global login_response, json_data

    if len(json_data)==0:
        res=authontication(username,password)
        login_response=res[0]
        json_data=res[1]

    try:
        if json_data.get("authenticated") != None:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            csrf_token = cookie_jar['csrftoken']
            session_id = cookie_jar['sessionid']

            # Header with session id
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
            	Safari/537.36 Edg/79.0.309.43",
                "cookie": f'sessionid={session_id};'
            }

            # Passing Instagram reel link as argument in Reel Module
            insta_reel = Reel(url)

            # Using scrape function and passing the headers
            insta_reel.scrape(headers=headers)

            video_name = (url.split('/'))[4]

            # Giving path where we want to download reel to the
            # download function
            insta_reel.download(fp=f"download\\{video_name}.mp4")

            return video_name
    except:
        return "None"