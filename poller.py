import time
import requests
import sys
import json

from constants import FRONTEND_POLLER_HOST
from util import print_debug, print_message
from start_diag_handler import StartDiagHandler
from start_model_handler import start_model_handler
from update_job_handler import UpdateJobHandler

def poll():

    params = {'request': 'next'}
    url = 'http://' + FRONTEND_POLLER_HOST + '/update/next/'
    try:
        job = requests.get(url, params).content
    except Exception as e:
        print_message("Error requesting job from frontend poller")
        print_debug(e)
        return

    try:
        options = json.loads(job.config_options)
    except Exception as e:
        print_debug(e)
        return

    run_type = options.get('run_type')
    if not run_type:
        print_message("No run type in job request")
        return

    if run_type == 'diagnostic':
        handler = StartDiagHandler(options)
    elif run_type == 'model':
        handler  = StartModelHandler(options)
    elif run_type == 'update':
        handler = UpdateJobHandler(options)
    else:
        print_message("Unrecognized request: {}".format(run_type))
        return

    try:
        response = handler.handle()
    except Exception as e:
        print_message("Error in job handler with options \n {}".format(options))
        print_debug(e)
        return
    try:
        handler.respond(response)
    except Exception as e:
        print_message("Error sending response to job \n {}".format(options))
        print_debug(e)
        return

    return


if __name__ == "__main__":
    while(True):
        poll()
        time.sleep(5)
