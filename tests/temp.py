from moodle_automate.context import check_config

config = {"logintoken": None, "username": None, "password": None}


def func(x): return x


res = check_config(func)
print(res)
