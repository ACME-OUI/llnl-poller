from subprocess import call


class StartDiagHandler(object):

    def __init__(self, config):
        self.config = config

    def handle(self, request):
        call_args = ['metadiags']
        for x in self.config:
            call_args.append(x)
            call_args.append(config.get(x))
        return call(call_args)

    def respond(self, response):
        return
