from tabulate import tabulate
from urllib.parse import urlparse, parse_qs
from context import RequestURL
import requests
import re

from const import MAINURL, CLNDRURL, SUBURL, SUBURL_REG, VIDEOURL_REG, RESOURCEURL_REG, ATTENDANCEURL_REG

def generator(soup):
        for data in ( resp.get_text() for resp in soup.find('div', {'class': 'calendarwrapper'}).find_all('a')):
                print(data) 

def calendarwrapper(session, headers):
        with RequestURL(CLNDRURL, session, headers) as soup:
                generator(soup)

                #for data in ( event.get_text().strip() for event in soup.find('div', {'class': 'calendarwrapper'}).find_all('a')):
                #            print(data)
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


def submitAttendance(targetURL, session, headers):

        payload = {
                 'status': '1561',
                 'submitbutton': 'Save+changes',
                 '_qf__mod_attendance_student_attendance_form': '1',
                 'mform_isexpanded_id_session': '1'}

        with RequestURL(targetURL, session, headers) as soup:
                target = soup.find('a', text='Submit attendance')['href']
                #for k, v in parse_qs(urlparse(target).query).items():
                #        payload[k] = ''.join(v)
                with RequestURL(target, session, headers) as soup2:
                        present = soup2.find('input', {'name': 'status', 'type': 'radio'}, text='Present')['value']
                        print(present)
                
        #html = session.get(targetURL, verify=False, headers=headers)
        #soup = BeautifulSoup(html.text, 'html5lib')



def subjectmaterial(session, headers, subId):
        with RequestURL(f'{SUBURL}{subId}', session, headers) as soup:
                links = soup.find_all('a', href=re.compile(VIDEOURL_REG + '|' + ATTENDANCEURL_REG + '|' + RESOURCEURL_REG)) 

                for link in links:
                        print(' '.join(link.get_text().split(' ')[:-1]))
                
                print(len(links))


