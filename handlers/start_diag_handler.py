from subprocess import Popen, PIPE
from constants import DIAG_PATH_PREFIX
from constants import FRONTEND_POLLER_HOST
from constants import DIAG_OUTPUT_PREFIX
from util import print_message, execute_in_virtualenv

import requests
import json
import os


class StartDiagHandler(object):

    def __init__(self, config):
        self.config = config
        self.call_args = self.sanitize_input()

    def handle(self):
        print_message(self.call_args, 'ok')
        output = execute_in_virtualenv(self.call_args)
        return output

    def respond(self, response):
        request = json.dumps({
            'id': self.config.get('id'),
            'request': 'complete',
            'output': response
        })
        url = 'http://' + FRONTEND_POLLER_HOST
        try:
            r = requests.post(url, request)
        except Exception as e:
            raise e
        return

    def sanitize_input(self):
        args = ['metadiags']
        path_prefix = "path=" + DIAG_PATH_PREFIX
        for x in self.config:
            option_key = ''
            option_val = ''
            if x == 'diag_type':
                option_key = '--package'
                # Check for valid package
                if self.config.get(x) != 'AMWG':
                    print_message("{} is not a valid package".format(self.config.get(x)))
                    return -1
                option_val = self.config.get(x)
            elif x == 'model_path':
                option_key = "--model "
                # Check for valid paths
                option_val = path_prefix + self.config.get(x) + ',climos=yes '
            elif x == 'obs_path':
                option_key = '--obs'
                # Check for valid obs path
                option_val = path_prefix + self.config.get(x) + ',climos=yes'
            elif x == 'outputdir':
                option_key = '--outputdir'
                # Check for valid outputdir
                run_suffix = '/' + self.config.get('user') + '/' + self.config.get('run_name')
                option_val = DIAG_OUTPUT_PREFIX + run_suffix + self.config.get(x)
                if os.path.exists(option_val) and not os.path.isdir(option_val):
                    print_message("Attempting to overwrite directory")
                    return -1
                if not os.path.exists(option_val):
                    os.makedirs(option_val)
            elif x == 'set':
                option_key = '--set'
                # Check for valid set
                option_val = self.config.get(x)
            #
            # etc etc etc moar options
            #
            else:
                print "Unrecognized option passed to diag handler \n{}".format(x)
                continue
            args.append(option_key)
            args.append(option_val)
        return args
