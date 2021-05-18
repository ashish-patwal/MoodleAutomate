import requests
import sys

from context import RequestURL, PostToURL
from parser import cmd_parser
from const import URL, MAINURL, params, headers, motive
from util import calenderEvents, listSubjects, submitAttendance, subjectList

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

                #    api_params['sesskey'] = soup.find('input', {'name': 'sesskey'})['value']

                # print(api_params)

                #responce = session.post(API, verify=False ,headers=headers, params=api_params, data=json.dumps(api_payload))
                # print(responce.status_code)
                # with open('result.json', 'w') as file:
                #    json.dump(responce.json(), file, indent=4, sort_keys=True)
                #format_str = json.dumps(responce.json(), indent=4)
                # print(format_str)

                if args.show_motive:
                    print(motive)

                elif args.list_subjects:
                    with RequestURL(MAINURL, session, headers) as soup:
                        sesskey = soup.find('input', {'name': 'sesskey'})['value']
                    listSubjects(session, headers, sesskey)

                elif args.mark_attendance:
                    submitAttendance(session, headers)

                elif args.show_events:
                    calenderEvents(session, headers)
