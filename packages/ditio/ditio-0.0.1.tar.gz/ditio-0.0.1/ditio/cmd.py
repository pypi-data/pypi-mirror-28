# uncompyle6 version 2.14.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 20 2017, 18:23:56) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/sven/0/_projects/dit.io/ditio/cmd.py
# Compiled at: 2018-01-05 19:46:48
import sys, traceback
from . import *
from . import site


def dispatch(opt, params, mappings):
    fn_keys = [ k for k in mappings.keys() if opt in  k.split(",")  ]
    if len(fn_keys) < 1:
        raise Exception('Invalid options : %s' % str(opt))

    if "--verbose" in fn_keys:
        fn_keys.remove("--verbose") 
        set_verbose(True) 
    fn = mappings[fn_keys[0]]
    fn(params)


class CommandLine(object):

    @staticmethod
    def extract(args):
        opts = [ o for o in args if o.find('-') ==0 ]
        params = [ p for p in args if p.find('-') != 0  ]
        return (opts, params)

    def preview(args):
        set_verbose(False) 
        opts, params = CommandLine.extract(args)

        notebook_fname = args[0]
        call(["site","new",".preview.io"])
        call(["publish",notebook_fname,".preview.io"])
        call(["site","index",".preview.io"])
        call(["site","server",".preview.io"])
        
    def publish(args):

        set_verbose(False) 
        opts, params = CommandLine.extract(args)
        if opts == []:
            cmd_publish_all(params)
        else:
            o = opts[0]
            dispatch(o, params, {'-a,--all': cmd_publish_all,
               '-m,--md': cmd_publish_markdown
               })

    def site(args):
        """ site new
        site index """
        opts, params = CommandLine.extract(args)
        p = params[0]
        if p in ('new', 'index','server'):
            site.cmd(params)
        else:
            print 'Command [%s] not recognised ' % p


call = lambda args: CommandLine.__getattribute__(CommandLine, args[0])(args[1:])
# okay decompiling cmd.pyc
