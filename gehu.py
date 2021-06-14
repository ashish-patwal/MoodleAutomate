import requests
import sys

from context import RequestURL, PostToURL, check_config
from parser import cmd_parser, write_config
from const import URL, MAINURL, config, headers, motive
from util import calenderEvents, listSubjects, submitAttendance

args = cmd_parser()

@check_config
def main():

    if len(sys.argv) == 1:
        print('Please provide arguments')

    else:
        if args.show_motive:
            print(motive)
            exit(0)

        with requests.Session() as session:
            with RequestURL(URL, session, headers) as soup:
                config['logintoken'] = soup.find(
                    'input', {'name': 'logintoken'})['value']

            print()
            print('Authenticating with Moodle')
            print('-'*20)

            with PostToURL(URL, session, headers, config) as responce:
                if responce.url == URL:
                    print('Wrong Credentials')
                    write_config()

                else:
                    headers.update(session.cookies.get_dict())
                    print('updated cookies for moodle session')
                    print('-'*20)

                    if args.list_subjects:
                        with RequestURL(MAINURL, session, headers) as soup:
                            sesskey = soup.find(
                                'input', {'name': 'sesskey'})['value']
                        listSubjects(session, headers, sesskey)

                    elif args.mark_attendance:
                        submitAttendance(session, headers)

                    elif args.show_events:
                        calenderEvents(session, headers)

if __name__ == '__main__':
    main()
