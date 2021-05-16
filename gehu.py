import requests
import json
import sys

from context import RequestURL, PostToURL
from parser import cmd_parser
from const import URL, MAINURL, params, headers, motive
from util import calenderEvents, listSubjects, submitAttendance, subjectList

API = 'http://45.116.207.79/moodle/lib/ajax/service.php?sesskey=jUndHEbdWs&info=core_fetch_notifications'

api_params = {'info': 'core_fetch_notifications'}

api_payload = {
        "index": 0,
        "methodname": "core_fetch_notifications",
        "args": {"contextid":10095}}

# payload = {
#        'sessid': '2542',
#        'sesskey': 'LAKRb1WMNT',
#        '_qf__mod_attendance_student_attendance_form': '1',
#        'mform_isexpanded_id_session': '1',
#        'status': '3365',
#        'submitbutton': 'Save changes'}

args = cmd_parser()

if len(sys.argv) == 1:
    print('Please provide arguments')

else:
    with requests.Session() as session:
        with RequestURL(URL, session, headers) as soup:
            params['logintoken'] = soup.find(
                'input', {'name': 'logintoken'})['value']

        print()
        print('Authenticating with Moodle')
        print('-'*20)

        with PostToURL(URL, session, headers, params) as responce:
            if responce.url == URL:
                print('Wrong Credentials')
            else:
                headers.update(session.cookies.get_dict())
                print('updated cookies for moodle session')
                print('-'*20)

                #with RequestURL(MAINURL, session, headers) as soup:
                #    api_params['sesskey'] = soup.find('input', {'name': 'sesskey'})['value']
                #    args = soup.find('head > script')
                #    print(args)
                    #api_params['args'] = {'contextid': args}

                #responce = session.post(API, verify=False ,headers=headers, params=api_params, json=api_payload)
                #print(responce.json())

                if args.show_motive:
                    print(motive)

                elif args.list_subjects:
                    subjectList(session, headers)

                elif args.mark_attendance:
                    submitAttendance(session, headers)

                elif args.show_events:
                    calenderEvents(session, headers)
