#!/usr/bin/env python
import time
import requests
import sys
import json

from constants import FRONTEND_POLLER_HOST
from util import print_debug
from util import print_message
from handlers.start_diag_handler import StartDiagHandler
from handlers.start_model_handler import StartModelHandler
from handlers.update_job_handler import UpdateJobHandler
from handlers.upload_output_handler import UploadOutputHandler


def poll():

    params = {'request': 'next'}
    url = 'http://' + FRONTEND_POLLER_HOST
    options = {}
    try:
        job = requests.get(url, params).content
        job = json.loads(job)
    except Exception as e:
        print_message("Error requesting job from frontend poller")
        print_debug(e)
        return -1, job['id']

    if not job:
        print_message('No new jobs')
        return -2, None

    try:
        options['user'] = job.get('user')
        options['run_name'] = job.get('run_name')
        options['job_id'] = job.get('job_id')
        if not job.get('diag_type'):
            options['diag_type'] = 'amwg'
        print_message('job options: {}'.format(options), 'ok')
    except Exception as e:
        print_debug(e)
        return -1, options['job_id']

    run_type = job.get('run_type')
    if not run_type:
        print_message("No run type in job request")
        return -1, None

    if run_type == 'diagnostic':
        try:
            sets = json.loads(job.get('diag_set'))
        except Exception as e:
            print_message('Unable to unpack diag_set')
            sets = '5'
        options['set'] = sets
        options['model_path'] = job.get('model_path')
        options['obs_path'] = job.get('obs_path')
        options['output_dir'] = job.get('output_dir')
        print_message('Got a new job with parameters:\n{}'.format(options), 'ok')
        handler = StartDiagHandler(options)
    elif run_type == 'model':
        handler = StartModelHandler(options)
    elif run_type == 'update':
        handler = UpdateJobHandler(options)
    elif run_type == 'upload_to_viewer':
        handler = UploadOutputHandler(options)
    else:
        print_message("Unrecognized request: {}".format(run_type))
        return -1, None

    try:
        response = handler.handle()
    except Exception as e:
        print_message("Error in job handler with options \n {}".format(options))
        print_debug(e)
        return -1, None
    try:
        print_message('Sending message to frontend poller: {}'.format(response))
        handler.respond(response)
    except Exception as e:
        print_message("Error sending response to job \n {}".format(options))
        print_debug(e)
        return -1, None

    return 0, None


if __name__ == "__main__":
    while(True):
        retval, id = poll()
        if retval == 0:
            continue
        if retval:
            print_message('Job run error')
            # send error message to frontend poller
            request = json.dumps({
                'job_id': id,
                'request': 'error',
            })
            url = 'http://' + FRONTEND_POLLER_HOST
            try:
                r = requests.post(url, request)
            except Exception as e:
                print_debug(e)
                continue
        time.sleep(5)
