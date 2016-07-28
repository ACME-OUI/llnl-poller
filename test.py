from util import virtualenv_execute

args = ['metadiags', '--help']
out = virtualenv_execute(args)
print out
