from subprocess import Popen, PIPE
from constants import DIAG_PATH_PREFIX, FRONTEND_POLLER_HOST
from util import print_message


class StartDiagHandler(object):

    def __init__(self, config):
        self.config = config
        self.call_args = self.sanitize_input()

    def handle(self):

        print_message(self.call_args, 'ok')
        if self.call_args:
            #
            #
            #
        return

    def respond(self, response):
        return

    def sanitize_input(self):
        args = []
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
                option_val = path_prefix + self.config.get(x) + ',climos=yes'
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