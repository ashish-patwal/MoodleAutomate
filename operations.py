from subprocess import Popen, PIPE
from urllib.parse import urlparse
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def play_video(player, url, session, headers):
    
    responce = session.get(url, verify=False, headers=headers)
    if urlparse(responce.url).netloc.find('drive.google.com') != -1:
        p = Popen(['brave', responce.url], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
    #    splits = (urlparse(responce.url).path).split('/')
    #    filename = splits[-2]
    #    driveurl = 'https://www.googleapis.com/drive/v3/files/' + filename + '?alt=media&key=' + key
    #    print(driveurl)
    #    p = Popen([player, driveurl])
    #    p.wait()


    elif urlparse(responce.url).netloc.find('youtube' != -1):
        p = Popen([player, responce.url], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        p.wait()
    
    else:
        print('ptanin kahan dali hai video')


def download_resource(url, session, headers):
    responce = session.get(url, verify=False, headers=headers)

    filename = os.path.basename(urlparse(responce.url).path)

    with open(filename, 'wb') as file:
        file.write(responce.content)

