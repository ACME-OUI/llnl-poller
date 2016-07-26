# An ACME dashboard job poller for the LLNL mini cluster

** setup ***

      git clone git@github.com:sterlingbaldwin/llnl-poller.git
      cd llnl-poller
      virtualenv env
      pip install -r -U requirements.txt
      python poller.py

Change the constants.py FRONTEND_POLLER_HOST variable to the hostname of the dashboard if its not
running on localhost.
