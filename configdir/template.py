SETTINGS_TEMPLATE = """

try:
    import configdir
    conf = configdir.get()
    print "Getting config: %s" % (conf,)
    cmod = __import__("configs.%s" % conf, {}, {}, [''])
    cmod_dict = dict([
        (k,v) for k,v in cmod.__dict__.iteritems() if not k.startswith('_')
    ])
    gd = globals()
    gd.update(cmod_dict)
    del gd
except Exception, e:
    print "FAILED: Cannot import configdir settings:\\n %s" % (e,)
    import sys
    sys.exit(1)
finally:
    if 'REQUIRED_VARS' in globals().keys():
        configdir.failOnMissing(globals(), REQUIRED_VARS)

"""
