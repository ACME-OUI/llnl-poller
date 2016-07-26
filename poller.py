import time
import requests
import sys
import json

from constants import FRONTEND_POLLER_HOST
from util import print_debug, print_message
from handlers.start_diag_handler import StartDiagHandler
from handlers.start_model_handler import StartModelHandler
from handlers.update_job_handler import UpdateJobHandler

def poll():

    params = {'request': 'next'}
    url = 'http://' + FRONTEND_POLLER_HOST + '/update/'
    try:
        job = requests.get(url, params).content
        job = json.loads(job)
        print_message(job, 'ok')
    except Exception as e:
        print_message("Error requesting job from frontend poller")
        print_debug(e)
        return

    if not job:
        print_message('No new jobs')
        return

    try:
        options = job.get('request_attr')
        print_message(options, 'ok')
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
