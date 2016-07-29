rimport unittest
import requests
import json

from constants import FRONTEND_POLLER_HOST
from poller import poll


class TestStartDiag(unittest.TestCase):

    def test_valid_run(self):
        # Prime the frontend poller with a job
        request = json.dumps({
            "user": "test",
            "request": "new",
            "run_type": "diagnostic",
            "run_name": "diag_test_run",
            "request_attr": {
                "obs_path": "/obs",
                "diag_type": "AMWG",
                "set": "5",
                "model_path": "/metadiags_test_data",
                "outputdir": "/diags_output"
            }
        })
        try:
            url = "http://" + FRONTEND_POLLER_HOST
            r = requests.post(url, request)
            print r.status_code
            self.assertTrue(r.status_code == 200)
        except Exception as e:
            raise
        self.assertTrue(poll() != -1)

if __name__ == '__main__':
    unittest.main()
