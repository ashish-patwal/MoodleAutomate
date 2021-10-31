import sys
import requests
from moodle_automate.parser import cmd_parser, write_config
from moodle_automate.const import URL, MAINURL, config, headers
from moodle_automate.context import RequestURL, PostToURL, check_config
from moodle_automate.util import calender_events, list_subjects, \
    submit_attendance, declare_motive

args = cmd_parser()


def get_sesskey(cur_session):
    """gets sesskey for current session"""
    with RequestURL(MAINURL, cur_session, headers) as soup:
        sesskey = soup.find(
            'input', {'name': 'sesskey'})['value']

        return sesskey


def login(cur_session):
    """logins to moodle"""
    with RequestURL(URL, cur_session, headers) as soup:
        config['logintoken'] = soup.find(
            'input', {'name': 'logintoken'})['value']

    print()
    print('-'*40)
    print('Authenticating with Moodle')
    print('-'*40)

    with PostToURL(URL, cur_session, headers, config) as response:
        if response.url == URL:
            print('Wrong Credentials')
            write_config()

        else:
            headers.update(cur_session.cookies.get_dict())
            print('-'*40)
            print('updated cookies for moodle session')
            print('-'*40)

    return cur_session


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
        updated_session = login(session)

        if args.list_subjects:
            list_subjects(updated_session, headers,
                          get_sesskey(updated_session))

        elif args.mark_attendance:
            submit_attendance(updated_session, headers)

        elif args.show_events:
            calender_events(updated_session, headers)


if __name__ == '__main__':
    main()
