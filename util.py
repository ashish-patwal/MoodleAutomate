import json
import os
import re
from requests import codes
import sys
from urllib.parse import urlparse, parse_qs
import threading
from tabulate import tabulate
from context import RequestURL, PostToURL, userChoiceError
from const import API, courses_api_params, courses_api_payload
from const import payload, CLNDRURL, SUBURL, VIDEOURL_REG, RESOURCEURL_REG, \
    ATTENDANCEURL_REG, MARKATTENDANCEURL, MOTIVE, MOTIVE_MSG
from operations import play_video, download_resource


def clear_screen() -> None:
    """clears the screen buffer"""
    os.system('clear' if os.name == 'posix' else 'cls')


def date_Time(soup) -> 'Data':
    """Function that returns the data of the events like time
            , date and name of event."""
    return (''.join(data.get_text().split()) for data in soup.find
            ('div', {'class': 'calendarwrapper'})
            .find_all('div', class_=re.compile('^row$')))


def declare_motive() -> None:
    """Function that declares my motive"""
    play_video(MOTIVE)
    print()
    print(MOTIVE_MSG)
    sys.exit(0)


def links(soup) -> 'links':
    """Function that returns the links of events for submitting attendance."""
    return (data.attrs['href'] for data in soup.find('div', {'class': 'maincalendar'}).find_all('a', href=re.compile(ATTENDANCEURL_REG)))


def submit_attendance(session, headers) -> None:
    """Submits the attendance for every calender event
    if submit attendance link is found."""
    print('Submitting attendance if any in calender')
    print('-'*20)
    with RequestURL(CLNDRURL, session, headers) as soup:
        for link in links(soup):
            threading.Thread(target=mark_attendance, args=(
                link, session, headers)).start()


def calender_events(session, headers) -> None:
    """Shows the calender events"""
    print('Showing upcoming events')
    print('-'*20)
    with RequestURL(CLNDRURL, session, headers) as soup:

        try:
            for counter, event in enumerate(date_Time(soup), 1):
                print(event)
                if counter % 3 == 0:
                    print('-'*20)
        except:
            print('No events as of now')
            print('-'*20)


def mark_attendance(target_url, session, headers) -> None:
    """Function that marks the attendance for every calender event."""
    payload_instance = dict(payload)

    with RequestURL(target_url, session, headers) as soup:
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
                present_value = soup2.find(
                    'input', {'name': 'status', 'type': 'radio'})['value']

                payload_instance.setdefault('status', present_value)

                with PostToURL(MARKATTENDANCEURL, session,
                               headers, payload_instance) as responce:
                    print(title)

                    if responce.status_code == codes['ok']:
                        print('Submitted Attendance successfully')
                    else:
                        print("Error happend : " + responce.status_code)
                    print('-'*20)


def list_subjects(session, headers, sesskey) -> None:
    """Prints the list of subjects from a json responce object."""

    courses_api_params['sesskey'] = sesskey
    responce = session.post(API, verify=False, headers=headers,
                            params=courses_api_params,
                            data=json.dumps(courses_api_payload))

    clear_screen()

    tab_data = [[counter, row['fullnamedisplay'], row['shortname'], row['id'],
                 row['progress']] for counter, row in
                enumerate(responce.json()[0]['data']['courses'], 1)]

    print(tabulate(tab_data, headers=[
          'S.No', 'Full Name', 'Short Name', 'ID', 'progress'],
        tablefmt='pretty'))

    try:

        choice = int(input('Enter choice : '))

        if choice not in range(1, len(tab_data) + 1):
            raise userChoiceError

        subject_material(session, headers, tab_data[choice-1][3])

    except (userChoiceError, ValueError):
        print('Invalid input. Check your choice.')

    except IndexError:
        print('value out of index')


def title_string_solver(title) -> 'String':
    """Returns the string after stripping unnecessay data."""

    return ' '.join(title.split()[:-1]) if len(title.split()) > 1 \
        else title.strip()


def type_parser(links, material) -> 'List':
    """Returns the list of links paired with their type"""

    searcher = re.compile('(' + VIDEOURL_REG + ')' + '|' +
                          '(' + ATTENDANCEURL_REG + ')' + '|'
                          + '(' + RESOURCEURL_REG + ')')

    display_list = []

    for link, col in zip(links, material):
        type = searcher.search(link)
        video, attendance, resource = type.groups()

        if video:
            display_list.append([col[0], col[1], 'video'])
        elif attendance:
            display_list.append([col[0], col[1], 'attendance'])
        else:
            display_list.append([col[0], col[1], 'resource'])

    return display_list


def subject_material(session, headers, sub_id) -> None:
    """Prints the resources for a particular subject."""

    with RequestURL(f'{SUBURL}{sub_id}', session, headers) as soup:
        links_data = soup.find_all('a', href=re.compile(
            VIDEOURL_REG + '|' + ATTENDANCEURL_REG + '|' + RESOURCEURL_REG))

        links_href = [link.attrs['href'] for link in links_data]

        datalist = [[counter, title_string_solver(link.get_text()),
                     link.attrs['href']]
                    for counter, link in enumerate(links_data, 1)]

        print_data_list = type_parser(links_href, datalist)

        clear_screen()

        print(tabulate(print_data_list, headers=[
              'S.No', 'Title', 'type'], tablefmt='pretty'))

        try:

            choice = input('Enter choice ( q to exit ): ')

            if choice in ('q', 'Q'):
                sys.exit(1)
            else:
                print()

            if int(choice) not in range(1, len(print_data_list) + 1) or \
                    not choice.isdigit():
                print(choice)
                raise userChoiceError

            baseurl = datalist[int(choice)-1][2]

            if print_data_list[int(choice)-1][2] == 'resource':
                download_resource(baseurl, session, headers)
            elif print_data_list[int(choice)-1][2] == 'video':
                play_video(baseurl, session, headers)
            elif print_data_list[int(choice)-1][2] == 'attendance':
                pass
            else:
                print('Something new just emerged . Contact the dev .')

        except userChoiceError:
            print('\nInvalid input. Check your responce.')

        except IndexError:
            print('value out of index')

        subject_material(session, headers, sub_id)
