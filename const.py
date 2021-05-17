URL = 'http://45.116.207.79/moodle/login/index.php'

MAINURL = "http://45.116.207.79/moodle/my/"

CLNDRURL = 'http://45.116.207.79/moodle/calendar/view.php?view=upcoming'

MARKATTENDANCEURL = 'http://45.116.207.79/moodle/mod/attendance/attendance.php'

SUBURL_REG = '^http://45\.116\.207\.79/moodle/course/view\.php\?id=[0-9]*$'
SUBURL = 'http://45.116.207.79/moodle/course/view.php?id='

VIDEOURL_REG = '^http://45\.116\.207\.79/moodle/mod/url/view\.php\?id=[0-9]*$'
VIDEOURL = 'http://45.116.207.79/moodle/mod/url/view.php?id='

RESOURCEURL_REG = '^http://45\.116\.207\.79/moodle/mod/resource/view\.php\?id=[0-9]*$'
RESOURCEURL = 'http://45.116.207.79/moodle/mod/resource/view.php?id='

ATTENDANCEURL_REG = '^http://45\.116\.207\.79/moodle/mod/attendance/view\.php\?id=[0-9]*$'
ATTENDANCEURL = 'http://45.116.207.79/moodle/mod/attendance/view.php?id='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

params = {'logintoken': 'Not updated', 'username': 'Your_username', 'password': 'Your_password'}

payload = {
    'submitbutton': 'Save+changes',
    '_qf__mod_attendance_student_attendance_form': '1',
    'mform_isexpanded_id_session': '1'}

API = 'http://45.116.207.79/moodle/lib/ajax/service.php'

courses_api_params = {'info': 'core_course_get_enrolled_courses_by_timeline_classification'}

courses_api_payload = '[{"index":0,"methodname":"core_course_get_enrolled_courses_by_timeline_classification","args":{"offset":0,"limit":0,"classification":"all","sort":"fullname","customfieldname":"","customfieldvalue":""}}]'


motive = '''
I wanna be the very best
Like no one ever was
To catch them is my real test
To train them is my cause

I will travel across the land
Searching far and wide
Each Pokemon to understand
The power that's inside

Pokemon, (gotta catch them all) it's you and me
I know it's my destiny (Pokemon)
Oh, you're my best friend
In a world we must defend

(Pokemon, gotta catch them all) a heart so true
Our courage will pull us through
You teach me and I'll teach you
(Pokemon) gotta catch 'em all
Gotta catch 'em all
Yeah

Every challenge along the way
With courage I will face
I will battle every day
To claim my rightful place

Come with me, the time is right
There's no better team
Arm-in-arm we'll win the fight
It's always been our dream

Pokemon (gotta catch them all) it's you and me
I know it's my destiny (Pokemon)
Oh, you're my best friend
In a world we must defend

(Pokemon, gotta catch them all) a heart so true
Our courage will pull us through
You teach me and I'll teach you
(Pokemon) gotta catch 'em all
Gotta catch 'em all
Gotta catch 'em all
Gotta catch 'em all
Gotta catch 'em all
Yeah!

Pokemon (gotta catch them all) it's you and me
I know it's my destiny (Pokemon)
Oh, you're my best friend
In a world we must defend

(Pokemon, gotta catch them all) a heart so true
Our courage will pull us through
You teach me and I'll teach you
(Pokemon) gotta catch 'em all
Gotta catch 'em all
(Pokemon!)

'''
