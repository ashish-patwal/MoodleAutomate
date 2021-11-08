import os
import re
import sys
import json
import threading
from requests import codes
from tabulate import tabulate
from urllib.parse import urlparse, parse_qs

from moodle_automate.operations import play_video, download_resource
from moodle_automate.context import RequestURL, PostToURL, UserChoiceError
from moodle_automate.downloaders.external_downloader import ExternalDownloader
from moodle_automate.const import API, courses_api_params, courses_api_payload
from moodle_automate.const import (
    MOTIVE,
    SUBURL,
    payload,
    CLNDRURL,
    MOTIVE_MSG,
    VIDEOURL_REG,
    RESOURCEURL_REG,
    MARKATTENDANCEURL,
    TOGGLE_COMPLETION,
    ATTENDANCEURL_REG,
    module_completion,
)


def clear_screen() -> None:
    """clears the screen buffer"""
    os.system("clear" if os.name == "posix" else "cls")


def current_events(soup) -> "Data":
    """Function that returns a list of current events bs4 object"""
    # pylint: disable=E0602
    return (
        data
        for data in soup.find("div", {"class": "calendarwrapper"}).find_all(
            "div", class_="description card-body"
        )
    )


def declare_motive() -> None:
    """Function that declares my motive"""
    # TODO: Condemm the use of play_video function in operations.py .
    # TODO: Get URL with requests .
    play_video(MOTIVE)
    print()
    print(MOTIVE_MSG)
    sys.exit(0)


def links(soup) -> "Links":
    """Function that returns the links of events for submitting attendance."""
    # pylint: disable=E0602
    return (
        data.attrs["href"]
        for data in soup.find("div", {"class": "maincalendar"}).find_all(
            "a", href=re.compile(ATTENDANCEURL_REG)
        )
    )


def submit_attendance(session, headers) -> None:
    """Submits the attendance for every calender event
    if submit attendance link is found."""
    clear_screen()
    print("Submitting attendance if any in calender")
    print("-" * 20)
    with RequestURL(CLNDRURL, session, headers) as soup:
        try:
            for link in next(links(soup)):
                threading.Thread(
                    target=mark_attendance, args=(link, session, headers)
                ).start()

        except StopIteration:
            print("No attendance event as of now")
            print("-" * 20)


def calender_events(session, headers) -> None:
    """Shows the calender events"""
    clear_screen()
    print("Showing upcoming events")
    print("-" * 20)
    with RequestURL(CLNDRURL, session, headers) as soup:

        try:
            for event in next(current_events(soup)):
                for row in event.find_all("div", class_=re.compile("^row$")):
                    print(row.get_text().strip())
                print("-" * 20)
                sys.stdout.flush()

        except StopIteration:
            print("No events as of now")
            print("-" * 20)


def mark_attendance(target_url, session, headers) -> None:
    """Function that marks the attendance for every calender event."""
    payload_instance = dict(payload)

    with RequestURL(target_url, session, headers) as soup:
        title = soup.title.string
        try:
            target = soup.find("a", text="Submit attendance")["href"]

        except TypeError:
            print(title)
            print("NO Submission Link")
            print("-" * 20)

        else:
            for key, value in parse_qs(urlparse(target).query).items():
                payload_instance[key] = "".join(value)

            with RequestURL(target, session, headers) as soup2:
                present_value = soup2.find(
                    "input", {"name": "status", "type": "radio"}
                )["value"]

                payload_instance.setdefault("status", present_value)

                with PostToURL(
                    MARKATTENDANCEURL, session, headers, payload_instance
                ) as responce:
                    print(title)

                    if responce.status_code == codes["ok"]:
                        print("Submitted Attendance successfully")
                    else:
                        print("Error happend : " + responce.status_code)
                    print("-" * 20)


def modules_download_range_resolver(range_list):
    """resolves the input choice given by user
    ex : 1 - 13, 22 , 47
    """

    comma_seperated = [item.strip() for item in range_list.split(",")]
    dash_list = []

    for item in comma_seperated:
        if "-" in item:
            tmp = [i.strip() for i in item.split("-")]
            if len(tmp) == 2:
                if int(tmp[0]) <= int(tmp[1]):
                    dash_list.extend(list(range(int(tmp[0]), int(tmp[1]) + 1)))
                else:
                    dash_list.extend(list(range(int(tmp[0]), int(tmp[1]) - 1, -1)))
        else:
            dash_list.append(int(item))

    return list(dict.fromkeys(dash_list))


def list_subjects(session, headers, sesskey, flagkey) -> None:
    """Prints the list of subjects from a json responce object."""

    courses_api_params["sesskey"] = sesskey
    responce = session.post(
        API,
        verify=False,
        headers=headers,
        params=courses_api_params,
        data=json.dumps(courses_api_payload),
    )

    clear_screen()

    tab_data = [
        [counter, row["fullnamedisplay"], row["shortname"], row["id"], row["progress"]]
        for counter, row in enumerate(responce.json()[0]["data"]["courses"], 1)
    ]

    print(
        tabulate(
            tab_data,
            headers=["S.No", "Full Name", "Short Name", "ID", "progress"],
            tablefmt="pretty",
        )
    )

    try:

        choice = input("Enter choice [ q/Q to quit ]: ")

        if choice.lower() == "q":
            return

        choice = int(choice)

        if choice not in range(1, len(tab_data) + 1):
            raise UserChoiceError

        subject_material(
            session,
            headers,
            tab_data[choice - 1],
            sesskey,
            flagkey,
        )

    except IndexError:
        print("value out of index. Check your choice...")

    except (UserChoiceError, ValueError):
        print("Invalid input. Check your choice...")

    list_subjects(session, headers, sesskey, flagkey)


def title_string_solver(title) -> str:
    """Returns the string after stripping unnecessay data."""

    return " ".join(title.split()[:-1]) if len(title.split()) > 1 else title.strip()


def type_parser(material) -> list:
    """Returns the list of links paired with their type"""

    searcher = re.compile(
        "("
        + VIDEOURL_REG
        + ")"
        + "|"
        + "("
        + ATTENDANCEURL_REG
        + ")"
        + "|"
        + "("
        + RESOURCEURL_REG
        + ")"
    )

    for data in material:
        types = searcher.search(data[2])
        if types:
            video, attendance, resource = types.groups()

            if video:
                data.append("video")
            elif attendance:
                data.append("attendance")
            elif resource:
                data.append("resource")
            else:
                data.append("None")

    return material


def mark_module_completion(session, headers, query):
    """check box completed modules / videos / resources / attendance"""

    with PostToURL(TOGGLE_COMPLETION, session, headers, query) as responce:
        if responce.status_code == codes["ok"]:
            return

        print("Error happend : " + responce.status_code)


def download_modules(session, headers, range_list, datalist, subject_directory):
    """main function to download modules from google drive and youtube"""

    instance = ExternalDownloader(subject_directory.strip())

    for data in datalist:
        if data[0] in range_list:
            if data[3] == "video":
                response = session.get(data[2], headers=headers, verify=False)
                instance.download_video(response.url)
                print("-" * 20)
                sys.stdout.flush()
            elif data[3] == "resource":
                download_resource(data[2], session, headers, subject_directory)
                print("-" * 20)
                sys.stdout.flush()

    input("Press any key to continue...")


def subject_material(
    session,
    headers,
    selected_subject_info,
    sesskey,
    flagkey,
) -> None:
    """Prints the resources for a particular subject."""

    with RequestURL(f"{SUBURL}{selected_subject_info[3]}", session, headers) as soup:
        links_data = soup.find_all(
            "a",
            href=re.compile(
                VIDEOURL_REG + "|" + ATTENDANCEURL_REG + "|" + RESOURCEURL_REG
            ),
        )

        datalist = [
            [counter, title_string_solver(link.get_text()), link.attrs["href"]]
            for counter, link in enumerate(links_data, 1)
        ]

        datalist = type_parser(datalist)

        clear_screen()

        print(
            tabulate(
                [[data[0], data[1], data[3]] for data in datalist],
                headers=["S.No", "Title", "url", "type"],
                tablefmt="pretty",
            )
        )

        try:

            if flagkey == "list_subjects":
                choice = input("Enter choice [ q/Q to quit ] : ")

                if choice.lower() == "q":
                    sys.exit(1)

                if (
                    int(choice) not in range(1, len(datalist) + 1)
                    or not choice.isdigit()
                ):
                    print(choice)
                    raise UserChoiceError

                baseurl = datalist[int(choice) - 1][2]
                module_completion["sesskey"] = sesskey
                module_completion["id"] = baseurl.split("=")[1]
                mark_module_completion(session, headers, module_completion)

                if datalist[int(choice) - 1][3] == "resource":
                    download_resource(
                        baseurl, session, headers, selected_subject_info[1]
                    )
                elif datalist[int(choice) - 1][3] == "video":
                    play_video(baseurl, session, headers)
                elif datalist[int(choice) - 1][3] == "attendance":
                    pass
                else:
                    print("Something new just emerged . Contact the dev .")

            elif flagkey == "download_modules":
                range_list = input("Enter modules to download [ q/Q to quit ]: ")

                if range_list.lower() == "q":
                    clear_screen()
                    sys.exit(0)

                range_list = modules_download_range_resolver(range_list)

                if range_list[-1] > len(datalist):
                    raise UserChoiceError

                download_modules(
                    session, headers, range_list, datalist, selected_subject_info[1]
                )

        except (UserChoiceError, ValueError):
            print("\nInvalid input. Check your responce.")

        except IndexError:
            print("value out of index")

        input("Press any key to continue...")
        # TODO: Addition of Quit statement and backspace for previous page
        subject_material(session, headers, selected_subject_info, sesskey, flagkey)
