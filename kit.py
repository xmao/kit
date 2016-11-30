#!/usr/bin/python

import os
import shutil
import tempfile
import subprocess

if 'KITROOT' in os.environ:
    KITROOT = os.environ['KITROOT']
else:
    KITROOT = os.path.join(
        os.path.dirname(__file__), 'scripts')

KIT_TYPES = {
    'awk':  '#!/usr/bin/env awk',
    'mathematica':  '#!/usr/bin/env MathematicaScript -script',
    'perl':  '#!/usr/bin/env perl',
    'python':  '#!/usr/bin/env python',
    'R':  '#!/usr/bin/env Rscript',
    'ruby':  '#!/usr/bin/env ruby',
    'sed':  '#!/usr/bin/env sed',
    'shell':  '#!/usr/bin/env sh',
}


def kit_cat(names, args):
    p = get_program(names)
    if os.path.isfile(p):
        os.system("cat %s" % p)


def kit_edit(names, args):
    def get_editor():
        return os.getenv('KIT_EDITOR') \
            or os.getenv('VISUAL') \
            or os.getenv('EDITOR') \
            or 'vi'

    p = get_program(names)
    f = tempfile.mkstemp(prefix='kit')
    if os.path.isfile(p):
        shutil.copy(p, f[1])

    failed = os.system('%s %s' % (get_editor(), f[1]))
    if not failed:
        shutil.copy(f[1], p)
        os.system('chmod a+x %s' % p)
    if os.path.isfile(f[1]):
        os.system('rm -rf %s' % f[1])


def kit_create(names, args):
    path = get_program(names)
    os.system('mkdir -p %s' % os.path.dirname(path))
    os.system('touch %s' % path)
    if '-t' in args:
        type = args[(args.index('-t') + 1)]
        if type in KIT_TYPES:
            f = open(path, 'w')
            print >>f, KIT_TYPES[type]
            f.close()
    kit_edit(names, args)

def kit_run(names, args):
        try:
            p = subprocess.Popen([get_program(names)] + args)
            retcode = p.wait()
        except KeyboardInterrupt, e:
            p.kill()
            sys.exit(1)
        except:
            raise
        else:
            sys.exit(retcode)

def kit_help(names, args):
    for l in file(get_program(names)):
        l = l.strip()
        if l.startswith('#'):
            if l == '#' or l.startswith('#!'):
                continue
            else:
                print l[1:].strip()
        else:
            break


def get_program(names):
    return os.path.join(KITROOT, *names)


def get_names_and_args(args):
    for i in range(len(args)):
        if os.path.isfile(get_program(args[:i + 1])):
            return args[:i + 1], args[i + 1:]
    return args, []

if __name__ == '__main__':
    import sys

    names, args = get_names_and_args(sys.argv[1:])

    KIT_METHODS = dict(
        [(k[4:], v) for k, v in vars().items() if k.startswith('kit_')])

    if '-h' in args:
        KIT_METHODS['help'](names)
    elif names[0] in KIT_METHODS:
        KIT_METHODS[names[0]](names[1:], args)
    elif not os.path.isfile(get_program(names)):
        if '-t' not in args:
            print "Supported script types are as follows:"
            types = KIT_TYPES.keys()
            for i in range(len(types)):
                print '%i: %s' % (i, types[i])
            idx = input('What type you will create (input index):')
            args.extend(['-t', types[idx]])
        kit_create(names, args)
    else:
        KIT_METHODS['run'](names, args)
