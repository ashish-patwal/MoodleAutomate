from moodle_automate.const import MOODLE_HOME, MOODLE_CONFIG, MOODLE_PREFERENCE, \
    config, preference
from moodle_automate.util import clear_screen
from moodle_automate.context import UserChoiceError
import os
import json
import argparse
import sys
from tabulate import tabulate
import inquirer
from inquirer.themes import GreenPassion


def config_setter() -> None:
    """Function that sets the config file"""

    clear_screen()
    load_config()
    load_preference()

    dict_options = {
        'username': config['username'],
        'password': config['password'],
        'player': preference['player'],
        'browser': preference['browser'],
        'download_dir': preference['download_dir'],
        'video_resolution': preference['video_resolution']
    }

    list_options = [[k, v] for k, v in dict_options.items()]

    print(tabulate(list_options, headers=[
          'type', 'Cur. Value'], tablefmt='pretty'))

    def resolve_value(answer):
        if answer['option'] != 'Exit':
            return f"Current Value : {dict_options[answer['option']]} -> New Value "
        clear_screen()
        sys.exit(0)

    def confirm_value(answer):
        return f"Confirm < {dict_options[answer['option']]} -> {answer['value']} > "

    def post_validate(answer, current):
        response = True
        if current == 'Yes':
            if answer['option'] in ('username', 'password'):
                config[answer['option']] = answer['value']
                write_config()
            elif answer['option'] in ('player', 'browser', 'video_resolution'):
                preference[answer['option']] = answer['value']
                write_preference()
            else:
                if os.path.exists(answer['value']):
                    preference['download_dir'] = answer['value']
                    write_preference()
                else:
                    response = False

        return response

    questions = [
        inquirer.List(
            'option',
            message='<< OPTIONS >> ',
            choices=[*list(dict_options.keys()), 'Exit']
        ),
        inquirer.Text(
            'value',
            message=resolve_value
        ),
        inquirer.List(
            'commit',
            message=confirm_value,
            choices=['Yes', 'No'],
            validate=post_validate,
            default=False
        ),
        inquirer.List(
            'postExit',
            message="Edit / Quit ",
            choices=['Edit', 'Quit']
        )
    ]

    answer = inquirer.prompt(questions, theme=GreenPassion())

    if answer['postExit'] == 'Edit':
        config_setter()

#        else:
#            raise userChoiceError

    print('\nConfiguration Saved')
    input()
    clear_screen()
    sys.exit(0)

#    except (userChoiceError, ValueError):
#        print('\nInvalid input. Check your choice.')
#        input()

#    config_setter()


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
        config_setter()
        exit(0)

    return args
