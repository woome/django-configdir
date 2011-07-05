import socket
import os
import logging
import pwd

def get():
    logger = logging.getLogger("configdir.get")
    h = socket.gethostname()
    # Pick the username from either an env var or from unix
    l = os.environ.get("CONFIG_USER", pwd.getpwuid(os.getuid())[0])
    wd = os.path.basename(os.getcwd())
    parts = (h, l, wd)
    conf = [confitem.replace('-', '_').replace('.', '_') \
                for confitem in parts] 
    name = "%s.%s__%s" % tuple(conf)
    return name


# Test required variables and fail if they aren't there
def failOnMissing(globalvars, REQUIRED_VARS):
    import sys
    do_fail = False
    for varname in REQUIRED_VARS:
        if varname not in globalvars:
            print >>sys.stderr, """ERROR: refusing to start django: %s was not present""" % varname
            do_fail = True
    if do_fail:
        # Not sure if this should raise an error
        print >>sys.stderr, """try: django_confighelper edit 
and set the correct value. Please check all settings values that are required."""
        sys.exit(1)

# End
