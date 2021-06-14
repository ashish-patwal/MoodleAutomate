import os
import json
import argparse
import sys
from tabulate import tabulate

from const import MOODLE_HOME, MOODLE_CONFIG, MOODLE_PREFERENCE, config, preference
from context import choiceRangeError

def configSetter() -> None:
    """Function that sets the config file"""
    os.system('clear' if os.uname().sysname == 'Linux' else 'cls')

    options = [[1, 'username', config['username']],
               [2, 'password', config['password']],
               [3, 'player', preference['player']],
               [4, 'browser', preference['browser']],
               [5, 'download_dir', preference['download_dir']]]

    print(tabulate(options, headers=['S.No', 'type', 'Cur. Value'], tablefmt='pretty'))

    try:

        choice = int(input('\nEnter a choice : '))

        if choice not in range(1,6):
            raise choiceRangeError

        newValue = input('\nEnter a new value : ')

        if choice == 1:
            config['username'] = newValue
            write_config()
        elif choice == 2:
            config['password'] = newValue
            write_config()
        elif choice == 3:
            preference['player'] = newValue
            write_preference()
        elif choice == 4:
            preference['browser'] = newValue
            write_preference()
        elif choice == 5:
            if os.path.exists(newValue):
                preference['download_dir'] = newValue
                write_preference()
            else:
                print('Path does not exist. Give an absolute path .')
                exit(0)

        print('\nConfiguration Saved')

    except choiceRangeError:
        print('\nInvalid input. Check your choice.')

    except ValueError:
        print('\nInvalid input. Use numerical keys.')
    # except Exception as e:
        # print(e)


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
    group.add_argument('--config', '-c', dest='config',
                       action='store_true', help='helps to set config variables')

    args = parser.parse_args(sys.argv[1:])

    if args.config:
        configSetter()
        exit(0)


    return args
