from constants import USER_DATA_PREFIX
from constants import FRONTEND_POLLER_HOST
from util import print_message, print_debug
from output_viewer.diagsviewer import DiagnosticsViewerClient


import requests
import json
import os


class UploadOutputHandler(object):

    def __init__(self, options=None):
        self.options = self.sanitize_input(options)
        print_message(self.options)

    def handle(self):
        client = DiagnosticsViewerClient(
            server=self.options['server'],
            cert=False)
        try:
            id, key = client.login(
                self.options['username'],
                self.options['password'])
        except Exception as e:
            print_debug(e)
            return -1
        path = self.options.get('path')
        dataset_id = client.upload_package(path)
        return dataset_id

    def respond(self, response):
        msg = "Sending complete job to the dashboard with response {}".format(response)
        print_message(msg, 'ok')
        request = json.dumps({
            'job_id': self.options.get('job_id'),
            'request': 'complete',
            'output': response
        })
        url = 'http://' + FRONTEND_POLLER_HOST
        try:
            r = requests.post(url, request)
        except Exception as e:
            raise e
        return

    def sanitize_input(self, options):
        validated_options = {}
        expected_params = [
            'server',
            'username',
            'password',
            'path',
            'job_id'
        ]
        for key in options:
            if key in expected_params:
                validated_options[key] = options[key]
            else:
                print_message('Unexpected option {}'.format(key))
        return validated_options
