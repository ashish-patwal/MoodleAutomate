from util import clearScreen
from context import userChoiceError
import os
import json
import argparse
import sys
from tabulate import tabulate

from const import MOODLE_HOME, MOODLE_CONFIG, MOODLE_PREFERENCE, \
    config, preference


def configSetter() -> None:
    """Function that sets the config file"""

    clearScreen()
    load_config()
    load_preference()

    options = [[1, 'username', config['username']],
               [2, 'password', config['password']],
               [3, 'player', preference['player']],
               [4, 'browser', preference['browser']],
               [5, 'download_dir', preference['download_dir']]]

    print(tabulate(options, headers=[
          'S.No', 'type', 'Cur. Value'], tablefmt='pretty'))

    try:

        configValue = None
        choice = input('\nEnter a choice 1 - 5 ( q to quit ): ')

        if choice in ('q', 'Q'):
            clearScreen()
            return

        configValue = input('\nEnter a new value : ')

        if choice == '1':
            config['username'] = configValue
            write_config()
        elif choice == '2':
            config['password'] = configValue
            write_config()
        elif choice == '3':
            preference['player'] = configValue
            write_preference()
        elif choice == '4':
            preference['browser'] = configValue
            write_preference()
        elif choice == '5':
            if os.path.exists(configValue):
                preference['download_dir'] = configValue
                write_preference()
            else:
                print('Path does not exist. Give an absolute path .')
                sys.exit(0)
        else:
            raise userChoiceError

        print('\nConfiguration Saved')
        input()

    except (userChoiceError, ValueError):
        print('\nInvalid input. Check your choice.')
        input()

    configSetter()


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
