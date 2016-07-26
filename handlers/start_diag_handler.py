from subprocess import call


class StartDiagHandler(object):

    def __init__(self, config):
        self.config = config

    def handle(self):
        call_args = ['metadiags']
        for x in self.config:
            option_key = ''
            option_val = ''
            if x == 'diag_type':
                option_key = 'SOME_DIAG_ARG'
                option_val = self.config.get(x)
            elif x == 'start_time':
                option_key = x
                option_val = self.config.get(x)
            #
            # etc etc etc moar options
            #

            else:
                print "Unrecognized option passed to diag handler \n{}".format(x)
                continue

            call_args.append(option_key)
            call_args.append(option_val)
        # return call(call_args)
        print call_args
        return

    def respond(self, response):
        return
