from tabulate import tabulate
from urllib.parse import urlparse, parse_qs
from requests import codes
import subprocess
import re
import threading

from operations import play_video
from context import RequestURL, PostToURL
from const import payload, MAINURL, CLNDRURL, SUBURL, SUBURL_REG, VIDEOURL_REG, RESOURCEURL_REG, ATTENDANCEURL_REG, MARKATTENDANCEURL


def dateAndTime(soup):
    # return [BeautifulSoup(data.select('div:nth-of-type(3)'), 'html5lib').get_text() for data in soup.select('div:is(.description .card-body)')]
    return (''.join(data.get_text().split()) for data in soup.find('div', {'class': 'calendarwrapper'}).find_all('div', class_=re.         compile('^row$')))


def Links(soup):
    return (data.attrs['href'] for data in soup.find('div', {'class': 'maincalendar'}).find_all('a', href=re.compile(ATTENDANCEURL_REG)))


def submitAttendance(session, headers):
    print('Submitting attendance if any in calender')
    print('-'*20)
    with RequestURL(CLNDRURL, session, headers) as soup:
        for link in Links(soup):
            threading.Thread(target=markAttendance, args=(
                link, session, headers)).start()


def calenderEvents(session, headers):
    print('Showing upcoming events')
    print('-'*20)
    with RequestURL(CLNDRURL, session, headers) as soup:
        for counter, event in enumerate(dateAndTime(soup), 1):
            print(event)
            if(counter % 3 == 0):
                print('-'*20)


def markAttendance(targetURL, session, headers):

    payload_instance = dict(payload)

    with RequestURL(targetURL, session, headers) as soup:
        print(soup.title.string)
        try:
            target = soup.find('a', text='Submit attendance')['href']
        except TypeError:
            print('NO Submission Link')
            print('-'*20)
        else:
            for k, v in parse_qs(urlparse(target).query).items():
                payload_instance[k] = ''.join(v)
            with RequestURL(target, session, headers) as soup2:
                presentValue = soup2.find(
                    'input', {'name': 'status', 'type': 'radio'})['value']
                # statusValue = presentValue.find_parent('input',{'name': 'status', 'type': 'radio'}).attrs['value']
                payload_instance.setdefault('status', presentValue)

                responce = PostToURL(
                    MARKATTENDANCEURL, session, headers, payload_instance)

                if responce.status_code == codes['ok']:
                    print('Submitted Attendance successfully')
                else:
                    print("Error happend : " + responce.status_code)
                print('-'*20)


def listSubjects(session, headers):
    with RequestURL(MAINURL, session, headers) as soup:

        subList = [[counter, event.get_text(), event.attrs['data-key']] for counter, event in enumerate(soup.find('nav', {
            'class': 'list-group'}).find_all('a', href=re.compile(SUBURL_REG)), 1)]

        print(tabulate(subList, headers=[
              'S.No', 'Subject', 'ID'], tablefmt='pretty'))
        choice = input('Enter choice : ')
        try:
            if (choice.isdigit()):
                subjectMaterial(session, headers, subList[int(choice)-1][2])
            else:
                print('Wrong Input')

        except IndexError:
            print('Wrong Input')


def titleStringSolver(title):
    return ' '.join(title.split()[:-1]) if len(title.split()) > 1 else title.strip()


def typeParser(links, material):

    searcher = re.compile('(' + VIDEOURL_REG + ')' + '|' +
                          '(' + ATTENDANCEURL_REG + ')' + '|' + '(' + RESOURCEURL_REG + ')')

    displayList = []

    for link, col in zip(links, material):
        typ = searcher.search(link)
        video, attendance, resource = typ.groups()

        if video:
            displayList.append([col[0], col[1], 'video'])
        elif attendance:
            displayList.append([col[0], col[1], 'attendance'])
        else:
            displayList.append([col[0], col[1], 'resource'])

    return displayList


def subjectMaterial(session, headers, subId):
    with RequestURL(f'{SUBURL}{subId}', session, headers) as soup:
        links = soup.find_all('a', href=re.compile(
            VIDEOURL_REG + '|' + ATTENDANCEURL_REG + '|' + RESOURCEURL_REG))

        linkss = [link.attrs['href'] for link in links]

        material = [[counter, titleStringSolver(link.get_text()), link.attrs['href']]
                    for counter, link in enumerate(links, 1)]

        printMaterial = typeParser(linkss, material)

        print(tabulate(printMaterial, headers=[
              'S.No', 'Title', 'type'], tablefmt='pretty'))

        choice = input('Enter choice : ')
        try:
            print('ok')
            if (choice.isdigit()):
                videourl = material[int(choice)-1][2]
                play_video('mpv', videourl, session, headers)

            else:
                print('Wrong Input')

        except:
            print('Error in util')
