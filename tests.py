import unittest
import requests

from util import virtualenv_execute
from constants import FRONTEND_POLLER_HOST


class TestStartDiag(unittest.TestCase):

    def test_valid_run(self):
        # Prime the frontend poller with a job
        request = {
            "user": "test",
            "run_type": "diagnostic",
            "run_name": "diag_test_run",
            "request_attr": {
                "obs_path": "/obs",
                "diag_type": "AMWG",
                "set": "5",
                "model_path": "/metadiags_test_data",
                "outputdir": "/diags_output"
            }
        }
        try:
            url = "http://" + FRONTEND_POLLER_HOST
            r = requests.post(url, request)
        except Exception as e:
            raise
        self.assertTrue(poll() == -1)

if __name__ == '__main__':
    unittest.main()
