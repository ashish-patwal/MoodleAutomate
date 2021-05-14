from bs4 import BeautifulSoup
import requests
import sys
import argparse
from const import URL, params, headers
from util import calenderEvents, listSubjects, submitAttendance, subjectmaterial

# payload = {
#        'sessid': '2542',
#        'sesskey': 'LAKRb1WMNT',
#        '_qf__mod_attendance_student_attendance_form': '1',
#        'mform_isexpanded_id_session': '1',
#        'status': '3365',
#        'submitbutton': 'Save changes'}


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument('--events', '-e', dest='show_events',
                   action='store_true', help='displays the upcoming events')
group.add_argument('--attendance', '-a', dest='mark_attendance',
                   action='store_true', help='marks attendance')
group.add_argument('--subjects', '-s', dest='list_subjects',
                   action='store_true', help='displays subject')

args = parser.parse_args()

if len(sys.argv) == 1:
    print('Please provide arguments')

else:
    with requests.Session() as session:
        html = session.get(URL, verify=False, headers=headers)
        soup = BeautifulSoup(html.content, 'html5lib')
        params['logintoken'] = soup.find(
            'input', {'name': 'logintoken'})['value']

        print()
        print('Authenticating with Moodle')
        print('-'*20)
        html2 = session.post(URL, verify=False, headers=headers, data=params)
        if html2.url == URL:
            print('Wrong Credentials')
        else:
            headers.update(session.cookies.get_dict())
            print('updated cookies for moodle session')
            print('-'*20)

            if args.list_subjects:
                listSubjects(session, headers)

            elif args.mark_attendance:
                submitAttendance(session, headers)

            elif args.show_events:
                calenderEvents(session, headers)
