from tabulate import tabulate
from urllib.parse import urlparse, parse_qs
from requests import codes
import json
import re
import threading
from timestamp import timestamp
from operations import play_video, download_resource
from context import RequestURL, PostToURL
from const import API, courses_api_params, courses_api_payload
from const import payload, MAINURL, CLNDRURL, SUBURL, SUBURL_REG, VIDEOURL_REG, RESOURCEURL_REG, ATTENDANCEURL_REG, MARKATTENDANCEURL


def dateAndTime(soup):
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

        try:
            for counter, event in enumerate(dateAndTime(soup), 1):
                print(event)
                if(counter % 3 == 0):
                    print('-'*20)
        except:
            print('No events as of now')
            print('-'*20)


def markAttendance(targetURL, session, headers):

    payload_instance = dict(payload)

    with RequestURL(targetURL, session, headers) as soup:
        title = soup.title.string
        try:
            target = soup.find('a', text='Submit attendance')['href']
        except TypeError:
            print(title)
            print('NO Submission Link')
            print('-'*20)
        else:
            for k, v in parse_qs(urlparse(target).query).items():
                payload_instance[k] = ''.join(v)
            with RequestURL(target, session, headers) as soup2:
                presentValue = soup2.find(
                    'input', {'name': 'status', 'type': 'radio'})['value']

                payload_instance.setdefault('status', presentValue)

                with PostToURL(MARKATTENDANCEURL, session, headers, payload_instance) as responce:

                    print(title)

                    if responce.status_code == codes['ok']:
                        print('Submitted Attendance successfully')
                    else:
                        print("Error happend : " + responce.status_code)
                    print('-'*20)


def subjectList(session, headers):
    with RequestURL(MAINURL, session, headers) as soup:

        subList = [[counter, event.get_text(), event.attrs['data-key']] for counter, event in enumerate(soup.find('ul',
                                                                                                                  class_=re.compile('list-group$')).find_all('a', href=re.compile(SUBURL_REG)), 1)]

        print(tabulate(subList, headers=[
              'S.No', 'Subject', 'ID'], tablefmt='pretty'))


def listSubjects(session, headers, sesskey):
    courses_api_params['sesskey'] = sesskey
    responce = session.post(API, verify=False, headers=headers,
                            params=courses_api_params, data=json.dumps(courses_api_payload))

    print()
    tab_data = [[counter, row['fullnamedisplay'], row['shortname'], row['id'], row['progress']]
                for counter, row in enumerate(responce.json()[0]['data']['courses'], 1)]
    print(tabulate(tab_data, headers=[
          'S.No', 'Full Name', 'Short Name', 'ID', 'progress'], tablefmt='pretty'))

    choice = input('Enter choice : ')

    try:
        if (choice.isdigit()):
            subjectMaterial(session, headers, tab_data[int(choice)-1][3])
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
                baseurl = material[int(choice)-1][2]
                if (printMaterial[int(choice)-1][2] == 'resource'):
                    print('resource')
                    download_resource(baseurl, session, headers)
                elif (printMaterial[int(choice)-1][2] == 'video'):
                    play_video('vlc', baseurl, session, headers)
                else:
                    print('its attendance')

            else:
                print('Wrong Input')

        except:
            print('Error in util')
