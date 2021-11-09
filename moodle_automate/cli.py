import sys
import requests

from moodle_automate.parser import cmd_parser
from moodle_automate.const import URL, MAINURL, config, headers
from moodle_automate.context import (
    PostToURL,
    RequestURL,
    check_config,
    FalseCredentialsError,
)

from moodle_automate.util import (
    list_subjects,
    declare_motive,
    calender_events,
    submit_attendance,
)

# Parses the flag options given to program and passes them as an instance to args
args = cmd_parser()


def get_sesskey(cur_session):
    """gets sesskey for current session"""
    with RequestURL(MAINURL, cur_session, headers) as soup:
        sesskey = soup.find("input", {"name": "sesskey"})["value"]

        return sesskey


def login(cur_session):
    """logins to moodle"""
    with RequestURL(URL, cur_session, headers) as soup:
        config["logintoken"] = soup.find("input", {"name": "logintoken"})["value"]

    print("\nAuthenticating with Moodle...")

    with PostToURL(URL, cur_session, headers, config) as response:
        if response.url == URL:
            """Since on failed authentication page redirects to the login page we get status[200] in place of authentication failed status code .
            Therefore need to compare redirected URLS to check if we were authenticated against the platform or not"""
            raise FalseCredentialsError

        headers.update(cur_session.cookies.get_dict())
        print("\nupdated cookies for moodle session...")

    return cur_session


@check_config
def cli():
    """cli function"""

    # --motive / -m
    if args.show_motive:
        # Something funny cooking here
        declare_motive()
        sys.exit(0)

    with requests.Session() as session:
        try:
            updated_session = login(session)
        except FalseCredentialsError:
            print("\nWrong Credentials . Authentication Failed ...")
            sys.exit(1)

        # --download / -d
        if args.download_modules:
            list_subjects(
                updated_session,
                headers,
                get_sesskey(updated_session),
                "download_modules",
            )

        # --subjects / -s
        elif args.list_subjects:
            list_subjects(
                updated_session, headers, get_sesskey(updated_session), "list_subjects"
            )

        # --attendance / -a
        elif args.mark_attendance:
            submit_attendance(updated_session, headers)

        # --events / -e
        elif args.show_events:
            calender_events(updated_session, headers)


def main():
    """main function"""
    try:
        cli()
    except Exception as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
