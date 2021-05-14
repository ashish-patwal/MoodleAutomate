from subprocess import Popen, PIPE
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def play_video(player, url, session, headers):
    responce = session.get(url, verify=False, headers=headers)
    print(responce.url)
    p = Popen([player, responce.url], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    p.wait()
