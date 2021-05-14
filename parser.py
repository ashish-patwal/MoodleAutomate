import argparse
import sys


def cmd_parser():
    parser = argparse.ArgumentParser(f'''

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

    args = parser.parse_args(sys.argv[1:])

    return args
