import os
import random
import tempfile
from moodle_automate.headers import get_random_header

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

MOODLE_HOME = os.path.join(os.getenv("HOME", tempfile.gettempdir()), ".moodle")

MOODLE_CONFIG = os.path.join(MOODLE_HOME, "config.json")

MOODLE_PREFERENCE = os.path.join(MOODLE_HOME, "preference.json")

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


URL = "http://45.116.207.79/moodle/login/index.php"

MAINURL = "http://45.116.207.79/moodle/my/"

CLNDRURL = "http://45.116.207.79/moodle/calendar/view.php?view=upcoming"

MARKATTENDANCEURL = "http://45.116.207.79/moodle/mod/attendance/attendance.php"

SUBURL_REG = "^http://45\.116\.207\.79/moodle/course/view\.php\?id=[0-9]*$"
SUBURL = "http://45.116.207.79/moodle/course/view.php?id="

VIDEOURL_REG = "^http://45\.116\.207\.79/moodle/mod/url/view\.php\?id=[0-9]*$"
VIDEOURL = "http://45.116.207.79/moodle/mod/url/view.php?id="

RESOURCEURL_REG = "^http://45\.116\.207\.79/moodle/mod/resource/view\.php\?id=[0-9]*$"
RESOURCEURL = "http://45.116.207.79/moodle/mod/resource/view.php?id="

ATTENDANCEURL_REG = (
    "^http://45\.116\.207\.79/moodle/mod/attendance/view\.php\?id=[0-9]*$"
)
ATTENDANCEURL = "http://45.116.207.79/moodle/mod/attendance/view.php?id="

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

headers = get_random_header()


config = {"logintoken": None, "username": None, "password": None}

preference = {
    "player": "vlc",
    "browser": "chrome",
    "download_dir": os.path.join(MOODLE_HOME, "downloads"),
    "video_download_dir": os.path.join(MOODLE_HOME, "videos"),
    "watch_video_resolution": "720",
    "download_video_resolution": "480",
}

payload = {
    "submitbutton": "Save+changes",
    "_qf__mod_attendance_student_attendance_form": "1",
    "mform_isexpanded_id_session": "1",
}


mpv_args = {
    "shuffle": "shuffle",
    "format": f"--ytdl-format=bestvideo[height<=?{preference['watch_video_resolution']}][fps<=?30]+bestaudio/best[height<={preference['watch_video_resolution']}]",
    "subLang": "--ytdl-raw-options=sub-lang=en,write-auto-sub=,yes-playlist=",
    "window": "--force-wondow=immediate",
}

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

API = "http://45.116.207.79/moodle/lib/ajax/service.php"

TOGGLE_COMPLETION = "http://45.116.207.79/moodle/course/togglecompletion.php"

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

module_completion = {"id": None, "completionstate": 1, "fromajax": 1, "sesskey": None}

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

message_counts_params = {
    "sesskey": None,
    "info": "core_message_get_conversation_counts,core_message_get_unread_conversation_counts",
}

message_counts_payload = [
    {
        "index": 0,
        "methodname": "core_message_get_conversation_counts",
        "args": {"userid": None},  # my user id
    },
    {
        "index": 1,
        "methodname": "core_message_get_unread_conversation_counts",
        "args": {"userid": None},  # my user id
    },
]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

message_conversation_btw_users_params = {
    "sesskey": None,
    "info": "core_message_get_conversation_between_users",
}

message_conversation_btw_users_payload = [
    {
        "index": 0,
        "methodname": "core_message_get_conversation_between_users",
        "args": {
            "userid": None,  # my user id
            "otheruserid": None,  # other user id
            "includecontactrequests": True,
            "includeprivacyinfo": True,
            "memberlimit": 0,
            "memberoffset": 0,
            "messagelimit": 100,
            "messageoffset": 0,
            "newestmessagesfirst": True,
        },
    }
]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

message_conversation_params = {
    "sesskey": None,
    "info": "core_message_get_conversations",
}

message_conversation_params = [
    {
        "index": 0,
        "methodname": "core_message_get_conversations",
        "args": {
            "userid": None,  # other user id <string format>
            "type": None,
            "limitnum": 51,
            "limitfrom": 0,
            "favourites": True,
            "mergeself": True,
        },
    }
]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

notification_api_params = {"sesskey": None, "info": "core_fetch_notifications"}

notification_api_payload = [
    {"index": 0, "methodname": "core_fetch_notifications", "args": {"contextid": None}}
]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

calender_api_params = {
    "sesskey": None,
    "info": "core_calendar_get_action_events_by_timesort",
}

calender_api_payload = [
    {
        "index": 0,
        "methodname": "core_calendar_get_action_events_by_timesort",
        "args": {
            "limitnum": 11,
            "timesortfrom": None,
            "timesortto": None,
            "limittononsuspendedevents": True,
        },
    }
]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

courses_api_params = {
    "sesskey": None,
    "info": "core_course_get_enrolled_courses_by_timeline_classification",
}

courses_api_payload = [
    {
        "index": 0,
        "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
        "args": {
            "offset": 0,
            "limit": 0,
            "classification": "all",
            "sort": "fullname",
            "customfieldname": "",
            "customfieldvalue": "",
        },
    }
]


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

MOTIVE = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
MOTIVE_MSG = "Sorry but you just got RICKROLLED by the master of mischief !!!"

# motive = '''
# I wanna be the very best
# Like no one ever was
# To catch them is my real test
# To train them is my cause
#
# I will travel across the land
# Searching far and wide
# Each Pokemon to understand
# The power that's inside
#
# Pokemon, (gotta catch them all) it's you and me
# I know it's my destiny (Pokemon)
# Oh, you're my best friend
# In a world we must defend
#
# (Pokemon, gotta catch them all) a heart so true
# Our courage will pull us through
# You teach me and I'll teach you
# (Pokemon) gotta catch 'em all
# Gotta catch 'em all
# Yeah
#
# Every challenge along the way
# With courage I will face
# I will battle every day
# To claim my rightful place
#
# Come with me, the time is right
# There's no better team
# Arm-in-arm we'll win the fight
# It's always been our dream
#
# Pokemon (gotta catch them all) it's you and me
# I know it's my destiny (Pokemon)
# Oh, you're my best friend
# In a world we must defend
#
# (Pokemon, gotta catch them all) a heart so true
# Our courage will pull us through
# You teach me and I'll teach you
# (Pokemon) gotta catch 'em all
# Gotta catch 'em all
# Gotta catch 'em all
# Gotta catch 'em all
# Gotta catch 'em all
# Yeah!
#
# Pokemon (gotta catch them all) it's you and me
# I know it's my destiny (Pokemon)
# Oh, you're my best friend
# In a world we must defend
#
# (Pokemon, gotta catch them all) a heart so true
# Our courage will pull us through
# You teach me and I'll teach you
# (Pokemon) gotta catch 'em all
# Gotta catch 'em all
# (Pokemon!)
#
# '''

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
