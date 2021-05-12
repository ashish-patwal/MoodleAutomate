from tabulate import tabulate
from context import RequestURL
import requests
import re

from const import MAINURL, CLNDRURL, SUBURL, SUBURL_REG, VIDEOURL, VIDEOURL_REG

def calendarwrapper(session, headers):
        with RequestURL(CLNDRURL, session, headers) as soup:
                for data in ( event.get_text().strip() for event in soup.find('div', {'class': 'calendarwrapper'}).find_all('a')):
                            print(data)
        #events = soup.find('div', {'class': 'Attendance'}).find_all('a') 
        #print(names)
        #print(events)
        #print(html.request.headers)

def subjectwrapper(session, headers):
        with RequestURL(MAINURL, session, headers) as soup:
        #events = soup.find('nav', {'class': 'list-group'}).find_all('a', href = re.compile('^http://45\.116\.207\.79/moodle/course/view\.php\?id=[0-9]*$'))
        #for event in events:
        #        print(event.get_text().strip())

                print(tabulate([ [event.get_text(), event.attrs['href']] for event in soup.find('nav', {'class': 'list-group'}).find_all('a', href = re.compile(SUBURL_REG))], headers=['subject', 'link'], tablefmt='pretty'))


def submitwrapper(session, headers, targetURL):
        pass
        #html = session.get(targetURL, verify=False, headers=headers)
        #soup = BeautifulSoup(html.text, 'html5lib')

        #target = soup.find('a', text='Submit attendance')
        #print(target)


def subjectmaterial(session, headers, subId):
        with RequestURL(f'{SUBURL}{subId}', session, headers) as soup:
                links = soup.find_all('a', href=re.compile(VIDEOURL_REG)) 

                for link in links:
                        print(link.attrs['href'])
                
                print(len(links))

