# An ACME dashboard job poller for the LLNL mini cluster
***Issues***
* The StartDiagHandler is the only implemented job request handler, next on the list are:
  - UpdateJobHandler
  - StopJobHandler
  - StartModelHandler
  - StopModelHandler



***setup***

      git clone git@github.com:sterlingbaldwin/llnl-poller.git
      cd llnl-poller
      virtualenv env
      pip install -r -U requirements.txt
      python poller.py

Change the constants.py FRONTEND_POLLER_HOST variable to the hostname of the dashboard if its not
running on localhost.

Install [UVCDAT](https://github.com/UV-CDAT/uvcdat/wiki/install)
Once uvcdat is installed

      source activate uvcdat
      pip install requests

***Running***

* The first step in the run process is to have the dashboard up and running
* In a new terminal run

      ./poller.py

* Use the dashboards run manager to create a new diagnostic run, hit start run, and select the new diagnostic run.
