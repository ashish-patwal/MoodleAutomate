from bs4 import BeautifulSoup
import requests
import re

from const import URL, params, headers
from util import calendarwrapper, subjectwrapper, submitwrapper, subjectmaterial

payload = {
        'sessid': '2524',
        'sesskey': 'LAKRb1WMNT',
        '_qf__mod_attendance_student_attendance_form': '1',
        'mform_isexpanded_id_session': '1',
        'status': '3365',
        'submitbutton': 'Save changes'}



with requests.Session() as session:
    html = session.get(URL, verify=False, headers=headers)
    soup = BeautifulSoup(html.content, 'html5lib')
    params['logintoken'] = soup.find('input', {'name': 'logintoken'})['value']
    
    html2 = session.post(URL, verify=False, headers=headers, data=params) 
    headers.update(session.cookies.get_dict())
    #calendarwrapper(session, headers) 
    #print('-'*20)
    #subjectwrapper(session, headers)
    #print('-'*20)
    #submitwrapper(session, headers, targetURL)
    subjectmaterial(session, headers ,'190')

    #r = session.post('http://45.116.207.79/moodle/mod/attendance/attendance.php', verify=False , headers=headers, data=payload)
    #print(r.status_code)





