import getpass
import json
import time
import smtplib
from math import trunc
import sys
import os
import logging

class ImproperlyConfigured(BaseException):
    pass


def __except__(exception, replacement_function):
    def _try_wrap(function):
        def __try_wrap(*__args, **__kwargs):
            try:
                return function(*__args, **__kwargs)
            except exception as e:
                return replacement_function(*__args, **__kwargs)
        return __try_wrap
    return _try_wrap


def send_gmail(recipient, subject, body, user=None, pwd=None):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('Email Sent.')
    except:
        print("failed to send mail")


def time_check(start):
    current_time = time.time()
    auto_refresh = False
    hours, rem = divmod(current_time - start, 3600)
    minutes, seconds = divmod(rem, 60)
    if minutes > 7:
        start = time.time()
        auto_refresh = True

    return start, auto_refresh


def time_elapsed(start, string_width=12):
    current_time = time.time()
    hours, rem = divmod(current_time - start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_string = f'{trunc(hours):02d}:{trunc(minutes):02d}:{trunc(seconds):02d}'
    return f'{time_string:>{string_width}}'


def time_bomb(countdown, package=(print, ("BOOM",)), action="", dots=3):
    action = action if action else package[0].__name__
    sys.stdout.write(f"{action} in {countdown}")
    sys.stdout.flush()
    for i in range(countdown - 1, -1, -1):
        for j in range(dots):
            time.sleep(1.0/(dots + 1))
            sys.stdout.write(".")
            sys.stdout.flush()
        time.sleep(.25)
        sys.stdout.write(str(i))
        sys.stdout.flush()
    print("")
    package[0](*package[1])

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def remove_if_exists(file_name):
    try:
        os.remove(file_name)
    except OSError:
        pass
