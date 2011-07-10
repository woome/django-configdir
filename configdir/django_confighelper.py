#!/usr/bin/env python

"""A module that auto creates django override configs"""

from __future__ import with_statement

import re
import os
import os.path
import sys
import types

import configdir


def print_value(v):
    if isinstance(v, types.ListType) or isinstance(v, types.TupleType):
        for val in v:
            print_value(val)
    else:
        print v


def setup_environment(filepath, depth):
    """setup our django 'app' environment"""
    from django.core.management import setup_environ
    import settings
    setup_environ(settings)


def config_module_to_path():
    module_name = configdir.get()
    pathname = "%s/configs/%s.py" % (os.getcwd(), module_name.replace(".", "/"))
    return pathname
    

def update_settings_file():
    from template import SETTINGS_TEMPLATE
    with open('settings.py', 'a') as fd:
        print >> fd, SETTINGS_TEMPLATE


def config_dir():
    try:
        from django.conf import settings
        os.environ["DJANGO_SETTINGS_MODULE"] = settings.__file__
    except ImportError:
        import os
        sys.path += [os.getcwd()]
        import settings
        os.environ["DJANGO_SETTINGS_MODULE"] = settings.__file__
        for s in dir(settings):
            if not s.startswith("_"):
                print "%s = %r" % (s, settings.__dict__[s])
    else:
        for s in dir(settings):
            if not s.startswith("_"):
                print "%s = %r" % (s, settings.__dict__[s])


def config_printval():
    import settings
    for val in sys.argv[2:]:
        try:
            print_value(settings.__dict__[val])
        except KeyError:
            print >>sys.stderr, "WARNING: %s does not exist in settings" % val
            sys.exit(1)
    
def make_default(path, fname=None, post_edit=True):
    path_values = re.search(r'(?P<dir>.*)\.(?P<userid>.*)__(?P<junk>.*)', configdir.get()).groupdict()
    default_config_path = "configs/defaults/%(userid)s.py" % path_values
    
    # check if it exists
    if os.path.exists(default_config_path):
        print "\nwriting default values from %s to current config file\n" % (default_config_path,)
        # check if one exists and delete it
        if os.path.exists(path):
            response = raw_input("you already have a config file - %s \nthis command will override it, do you wish to continue [y/n]: " % path)
            while response not in ('y', 'n'):
                response = raw_input('choose only one of [y/n]: ')
            if response == 'n': sys.exit(1)
            os.remove(path)
        make_file(path)
        with open(path, 'w') as fd:
            fd.write(open(default_config_path, 'r').read())
        if post_edit:
            run_editor(path)
    else:
        print >>sys.stderr, "\ndefault config - %s does not exist. \nadd one or manually edit your local config.\n" % default_config_path


def make_file(pathname):
    try:
        try:
           os.makedirs(os.path.dirname(pathname))
        except Exception, e:
           print >>sys.stdout, "%s" % (e,)

        if os.path.exists(pathname):
            print >>sys.stderr, "%s already exists, try the 'edit' command"  % pathname
            sys.exit(1)

        # Otherwise, setup default
        with open(pathname, "w") as fd:
            print >> fd, "# local config settings go here\n\nDEBUG=True\n"
            # Make a default module if none exists
            while pathname != os.getcwd():
                pathname = os.path.dirname(pathname)
                ipath = "%s/__init__.py" % pathname
                if not os.path.exists(ipath):
                    with open(ipath, 'w') as fid:
                        print >> fid, """# module init file """

    except Exception, e:
        print str(e)

def run_editor(path):
    """Run whatever system editor you have"""

    def guardedexec(variable, cmd):
        if variable in os.environ.keys():
            r = os.system(cmd)
            if r == 0:
                return
        raise Exception()

    try:
        guardedexec("EDITOR", "$EDITOR %s" % path)
    except Exception, e:
        try:
            guardedexec("VISUAL", "$VISUAL %s" % path)
        except Exception:
            os.system("editor %s" % path)

def main():
    import sys
    path = config_module_to_path()    
    if "edit" in sys.argv:
        run_editor(path)
    elif "updatesettings" in sys.argv:
        update_settings_file()
    elif "default" in sys.argv:
        make_default(path, post_edit=('-n' not in sys.argv))
    elif "print" in sys.argv:
        print path
    elif "cat" in sys.argv:
        with open(path, 'r') as fd:
            print "".join(fd.readlines())
    elif "printval" in sys.argv or "pv" in sys.argv:
        config_printval()
    elif "dir" in sys.argv:
        print config_dir()
    elif "help" in sys.argv:
        print """django_confighelper
        
django_confighelper updatesettings        
django_confighelper edit
django_confighelper print
django_confighelper default {default_config_file}
django_confighelper pv       {DJANGO_SETTING_NAME}
django_confighelper printval {DJANGO_SETTING_NAME}
django_confighelper setval {DJANGO_SETTING_NAME VALUE}

A tool for helping with override Django configs.

django_confighelper on it's own creates a config for the current django
instance based on the current hostname, the current name of the
effective uid and the current directory in which the django instance
is sitting:

  config/hostname/euidname__dirname.py

If the config already exists django_confighelper exits with a warning.

The 'edit' subcommand attempts to start a system editor on the
config. It first tries the environment variable $EDITOR and then
switches to "editor" from the execution path.

The 'print' subcommand prints the filename of the config file. This is
so you can script further interactions, for example:

  echo "CONFIG_SPECIAL=True" >> $(django_confighelper print)

The 'default' subcommand looks for a default config file in 
config/defaults/$user.py and if it exists, it creates a config using
the values contained there in. It opens the newly created file just
in case you need to change some values - like FRONTEND_PORT e.t.c

The 'printval' subcommand prints the value of a DJANGO config setting
after the config has been applied. For example:

  django_confighelper printval DATABASE_HOST

prints out the setting of the database host.

In addition to these behaviours django_confighelper tries to help find
the initial DJANGO_PATH_DIR by looking for the envrionment variable:

   DJANGO_PATH_DIR

and if that isn't found checking for the existance of the path:
  
   $HOME/django-hg-1.1

and using that if found.

It also writes commented out values for:

    FRONTEND_PORT
    BACKEND_PORT
"""

#The 'setval' subcommand sets the value of the specified DJANGO config
#variable, directly in the config override file.

    else:
        make_file(path)
        

if __name__ == '__main__':
    main()

# End
