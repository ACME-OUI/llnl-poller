#!/usr/bin/env python
import time
import requests
import sys
import json

from constants import FRONTEND_POLLER_HOST
from util import print_debug, print_message
from handlers.start_diag_handler import StartDiagHandler
from handlers.start_model_handler import StartModelHandler
from handlers.update_job_handler import UpdateJobHandler
from handlers.upload_output_handler import UploadOutputHandler


def poll():

    params = {'request': 'next'}
    url = 'http://' + FRONTEND_POLLER_HOST
    try:
        job = requests.get(url, params).content
        job = json.loads(job)
        print_message(job, 'ok')
    except Exception as e:
        print_message("Error requesting job from frontend poller")
        print_debug(e)
        return -1

    if not job:
        print_message('No new jobs')
        return 0

    try:
        options = job.get('request_attr')
        options['user'] = job.get('user')
        options['run_name'] = job.get('run_name')
        options['job_id'] = job.get('job_id')
        print_message('job options: {}'.format(options), 'ok')
    except Exception as e:
        print_debug(e)
        return -1

    run_type = job.get('run_type')
    if not run_type:
        print_message("No run type in job request")
        return -1

    if run_type == 'diagnostic':
        handler = StartDiagHandler(options)
    elif run_type == 'model':
        handler = StartModelHandler(options)
    elif run_type == 'update':
        handler = UpdateJobHandler(options)
    elif run_type == 'upload_to_viewer':
        handler = UploadOutputHandler(options)
    else:
        print_message("Unrecognized request: {}".format(run_type))
        return -1

    try:
        response = handler.handle()
    except Exception as e:
        print_message("Error in job handler with options \n {}".format(options))
        print_debug(e)
        return -1
    try:
        print_message('Sending message to frontend poller: {}'.format(response))
        handler.respond(response)
    except Exception as e:
        print_message("Error sending response to job \n {}".format(options))
        print_debug(e)
        return -1

    return 0


if __name__ == "__main__":
    while(True):
        retval = poll()
        if retval:
            print_message('Job run error')
            # send error message to frontend poller
        time.sleep(5)
