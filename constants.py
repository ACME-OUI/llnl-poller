#
# A list of constants for the job poller
#

# hostname of the server running the frontend poller application
FRONTEND_POLLER_HOST = 'localhost:8000/poller/update/'

# diagnostic path base
DIAG_PATH_PREFIX = '$HOME/diags'

# hardcoded directory prefix for where to move the output to
# Im hard coding this instead of doing relative paths
# because the poller and the dashboard should live on
# differenct servers with a jointly mounted drive
# but the configuration hasnt been hammered out yet
DIAG_OUTPUT_PREFIX = '$HOME/Projects/acme-web-fe/run_manager/run_scripts/'
