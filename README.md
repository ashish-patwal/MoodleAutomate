# MOODLE AUTOMATE

## A CLI Python program to automate and minimize ease of moodle platform studying

A CLI tool that helps you to take classes online in the minimalistic way possible .

Watch online videos directly streaming to your local media player , take attendance and watch upcoming events without the use of your browser .
Directly download any resources available on the online platform without opening your browser .

_With all due regards this is only a spaghetti code, feel free to add any features you want and modify it . Just give due credits and do mention the original source code so other people can also fork from this ._

## Installation :

1. Clone the repository

```bash
git clone https://github.com/ashish-patwal/MoodleAutomate.git
```

2. Cd into the repository

```bash
cd MoodleAutomate/
```

3. Install required modules with requirements.txt

```bash
pip install -r requirements.txt
```

## Prerequisite :

_*Python library needed :*_<br>

- bs4
- urllib3
- html5lib
- inquirer
- tabulate
- soupsieve

## BASIC USAGE :

**Make sure your are in _root_ MoodleAutomate folder ( Not moodle_automate )**

_All the flags ( -h, -c, -s, -a, -e, -d) are mutually exclusive < you can only use one flag at a time not together >_

- Display Help

```bash
python -m moodle_automate.cli -h
```

- Set up Config

```bash
python -m moodle_automate.cli -c
```

- List subjects to watch video lectures and download resources

```bash
python -m moodle_automate.cli -s
```

- Download video lectures and resources ( pdf, pptx etc )

```bash
python -m moodle_automate.cli -d
```

- Show upcoming events if available

```bash
python -m mooodle_automate.cli -e
```

- Take attendance if available

```bash
python -m moodle_automate.cli -a
```

## Demo

*https://user-images.githubusercontent.com/63491234/140880423-19885a0c-5f23-46f3-a996-b592a4d11cab.mp4*

## Screenshots

![config](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/config.png)
![config_download_directory1](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/config_download_directory.png)
![config_download_directory2](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/config_download_directory2.png)
![download_video_running](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/download_video_running.png)
![download_video_completed](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/download_video_completed.png)
![subjects](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/subjects.png)
![module_resources](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/module_resources.png)
![topics](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/topics.png)
![events](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/events.png)
![no_attendance_availble](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/no_attendance_available.png)
![mpvj](https://raw.githubusercontent.com/ashish-patwal/MoodleAutomate/master/Screenshots/mpv.png)
