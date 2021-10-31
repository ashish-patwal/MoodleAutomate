from moodle_automate.util import calender_events, list_subjects, submit_attendance, declare_motive
from moodle_automate.const import URL, MAINURL, config, headers
from moodle_automate.parser import cmd_parser, write_config
from moodle_automate.context import RequestURL, PostToURL, check_config
import requests
import sys

args = cmd_parser()


@check_config
def main():
    """main function"""

    if len(sys.argv) == 1:
        print('Please provide arguments')
        sys.exit(1)

    else:
        if args.show_motive:
            declare_motive()

    with requests.Session() as session:
        with RequestURL(URL, session, headers) as soup:
            config['logintoken'] = soup.find(
                'input', {'name': 'logintoken'})['value']

        print()
        print('Authenticating with Moodle')
        print('-'*20)

        with PostToURL(URL, session, headers, config) as response:
            if response.url == URL:
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
                    list_subjects(session, headers, sesskey)

                elif args.mark_attendance:
                    submit_attendance(session, headers)

                elif args.show_events:
                    calender_events(session, headers)


if __name__ == '__main__':
    main()
