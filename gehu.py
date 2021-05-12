from bs4 import BeautifulSoup
import requests
import re

from const import URL, params, headers
from util import calendarwrapper, subjectwrapper, submitwrapper, subjectmaterial



with requests.Session() as session:
    html = session.get(URL, verify=False, headers=headers)
    soup = BeautifulSoup(html.content, 'html5lib')
    params['logintoken'] = soup.find('input', {'name': 'logintoken'})['value']
    
    html2 = session.post(URL, verify=False, headers=headers, data=params) 
    headers.update(session.cookies.get_dict())
    #calendarwrapper(session, headers) 
    #print('-'*20)
    #subjectwrapper(session, headers)
    #print('-'*20)
    #submitwrapper(session, headers, targetURL)
    subjectmaterial(session, headers ,'190')
    




