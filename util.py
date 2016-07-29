import sys
import traceback
import os
import shlex
from subprocess import Popen, PIPE


def print_debug(e):
    print '1', e.__doc__
    print '2', sys.exc_info()
    print '3', sys.exc_info()[0]
    print '4', sys.exc_info()[1]
    print '5', traceback.tb_lineno(sys.exc_info()[2])
    ex_type, ex, tb = sys.exc_info()
    print '6', traceback.print_tb(tb)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_message(message, status='error'):
    if status == 'error':
        print colors.FAIL + '[-] ' + colors.ENDC + colors.BOLD + str(message) + colors.ENDC
    elif status == 'ok':
        print colors.OKGREEN + '[+] ' + colors.ENDC + str(message)


def execute_in_virtualenv(command_list):
    from textwrap import dedent

    commands = dedent(r'''
        from subprocess import Popen, PIPE
        p = Popen(''' + str(command_list) + ''', stdout=PIPE, stderr=PIPE, shell=False)
        print p.communicate()
        ''')

    command_template = '/bin/bash -c "source activate uvcdat && python -"'
    command = shlex.split(command_template)
    process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    return process.communicate(commands)
