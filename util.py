from tabulate import tabulate
from bs4 import BeautifulSoup
import requests
import re

from const import MAINURL, CLNDRURL, SUBURL, SUBURL_REG, VIDEOURL, VIDEOURL_REG

def calendarwrapper(session, headers):
        html = session.get(CLNDRURL, verify=False, headers=headers)
        soup = BeautifulSoup(html.text, 'html5lib')
        for data in ( event.get_text().strip() for event in soup.find('div', {'class': 'calendarwrapper'}).find_all('a')):
                    print(data)
        #events = soup.find('div', {'class': 'Attendance'}).find_all('a') 
        #print(names)
        #print(events)
        #print(html.request.headers)

def subjectwrapper(session, headers):
        html = session.get(MAINURL, verify=False, headers=headers)
        soup = BeautifulSoup(html.text, 'html5lib')
        #events = soup.find('nav', {'class': 'list-group'}).find_all('a', href = re.compile('^http://45\.116\.207\.79/moodle/course/view\.php\?id=[0-9]*$'))
        #for event in events:
        #        print(event.get_text().strip())

        print(tabulate([ [event.get_text(), event.attrs['href']] for event in soup.find('nav', {'class': 'list-group'}).find_all('a', href = re.compile(SUBURL_REG))], headers=['subject', 'link'], tablefmt='pretty'))


def submitwrapper(session, headers, targetURL):
        html = session.get(targetURL, verify=False, headers=headers)
        soup = BeautifulSoup(html.text, 'html5lib')

        target = soup.find('a', text='Submit attendance')
        print(target)


def subjectmaterial(session, headers, subId):
        html = session.get(f'{SUBURL}{subId}', verify=False, headers=headers)
        soup = BeautifulSoup(html.text, 'html5lib')
        links = soup.find_all('a', href=re.compile(VIDEOURL_REG)) 

        for link in links:
                print(link.attrs['href'])
        
        print(len(links))

