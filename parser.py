import os
import json
import argparse
import sys

from const import MOODLE_HOME, MOODLE_CONFIG, MOODLE_PREFERENCE, config, preference

def load_config():
    if not os.path.exists(MOODLE_CONFIG):
        return

    try:
        with open(MOODLE_CONFIG, 'r') as f:
            config.update(json.load(f))
    except json.JSONDecodeError:
        write_config()

def write_config():
    if not os.path.exists(MOODLE_HOME):
        os.mkdir(MOODLE_HOME)

    with open(MOODLE_CONFIG, 'w') as f:
        f.write(json.dumps(config))


def load_preference():
    if not os.path.exists(MOODLE_PREFERENCE):
        return

    try:
        with open(MOODLE_PREFERENCE, 'r') as f:
            preference.update(json.load(f))
    except json.JSONDecodeError:
        write_preference()


def write_preference():
    if not os.path.exists(MOODLE_HOME):
        os.mkdir(MOODLE_HOME)

    with open(MOODLE_PREFERENCE, 'w') as f:
        f.write(json.dumps(preference))

def cmd_parser() -> 'argument':

    load_config()
    load_preference()

    """Parses the command line arguments."""
    parser = argparse.ArgumentParser('''

    MOODLE AUTOMATOR

    ''')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--events', '-e', dest='show_events',
                       action='store_true', help='displays the upcoming events')
    group.add_argument('--attendance', '-a', dest='mark_attendance',
                       action='store_true', help='marks attendance')
    group.add_argument('--subjects', '-s', dest='list_subjects',
                       action='store_true', help='displays subject')
    group.add_argument('--motive', '-m', dest='show_motive',
                       action='store_true', help='displays my motive')
    parser.add_argument('--username', '-u', dest='username',
                       action='store', help='saves username')
    parser.add_argument('--password', '-p', dest='password',
                       action='store', help='saves password')
    parser.add_argument('--player', '-P', dest='player',
                        action='store', help='value for media player')
    parser.add_argument('--browser', '-b', dest='browser',
                        action='store', help='value for browser')
    parser.add_argument('--download-dir', '-d', dest='downloadDir',
                        action='store', help='location of download directory')

    args = parser.parse_args(sys.argv[1:])

    if args.username is not None:
        config['username'] = args.username
        write_config()

    if args.password is not None:
        config['password'] = args.password
        write_config()

    if args.player is not None:
        preference['player'] = args.player
        write_preference()

    if args.browser is not None:
        preference['browser'] = args.browser
        write_preference()

    if args.downloadDir is not None:
        if os.path.exists(args.downloadDir):
            preference['download_dir'] = args.downloadDir
            write_preference()
        else:
            print('Path does not exist. Give an absolute path .')
            exit(0)

    if args.username or args.password or args.player or args.browser \
       or args.downloadDir:
        print()
        print('Configuration saved')
        exit(0)


    return args
