# basic functions for logging to Apache error log

import sys

def debug(s):
        sys.stderr.write('log: %s\n' % s)
