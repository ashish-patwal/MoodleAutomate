from moodle_automate.context import check_config
from moodle_automate.parser import load_config

load_config()


def func():
    pass


res = check_config(func)

print(res())
print(type(res()))
print(callable(res))
