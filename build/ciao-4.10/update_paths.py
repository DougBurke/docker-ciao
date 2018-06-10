#!/usr/bin/env python

"""
Change the contents of files in the CIAO directory system to replace
hard-coded paths of the build location to the current install
location.

This script requires that CIAO has already been installed since it
uses the environment variable $ASCDS_INSTALL to both find the
files to change and to work out what the install location is.

There is some attempt to protect against problems during over-writing
the files (in that the backup file is created before the file is
over-written), but it has not been written to be robust in the case
of problems. Keep the original tarballs so that CIAO can be re-installed
if necessary!

"""

import glob
import os
import re
import sys


ascds_install = os.environ['ASCDS_INSTALL']
if ascds_install is None:
    raise IOError("Unable to find $ASCDS_INSTALL: has CIAO been started?")

if ' ' in ascds_install:
    raise IOError("$ASCDS_INSTALL contains a space; this has not been tested")


# set to True for testing; will write the files to the local directory
# rather than over-write. This can be set when calling the script.
#
hack_filenames = False


# Replacement; this is hard-coded until it becomes obvious
# a more-general approach is workable.
#
def make_big_table(platname):
    """platname is the CIAO symbol for the platform - e.g. 'Linux64'

    This is currently linux-only
    """

    # I have no idea what the rules for this name are...
    # The HEA-installed versions (Linux64 and LinuxP3) have the
    # following setup.
    #
    # Maybe it would be best to either include all variants,
    # or just replace any directory name (e.g. use something like
    # [^/]+). Yeah, let's do that.
    pyname = platname
    if sys.version_info.major > 2:
        pyname = 'LinuxP3'

    d = {'p': platname,
         'pyname': pyname,
         'pyver': '{}.{}.{}'.format(sys.version_info.major,
                                    sys.version_info.minor,
                                    sys.version_info.micro)
         }

    # This needs to return an ordered set of pairs, to ensure
    # they get applied in the right order.
    #
    # Could force this by sorting on the length of the replacement
    # text (longest first) as that should be sufficient ordering.
    #
    # There are some patterns it does not catch - for instance
    # in the _sysconfigdata file there's abs_builddir/abs_srcdir
    # which are set to .../Python-<version> - i.e. without the
    # trailing package designator - that this does not handle
    # well, but it's unclear what this should be anyway, so
    # leave as is (the output is then to ots/Python-<version>
    # so it's easy to find and not going to point to an existing
    # directory).
    #
    return [(re.compile(k.format(**d)),
             os.path.join(ascds_install, v))
            for k, v in
            [
                # should be clever, but this is easier
                #
                # For the version strings tend not to be bothered about
                # . being taken to mean "any character", but it is
                # more important to protect it outside of "Python-<version>"
                # or "ciao-<version>", particularly when followed by
                # something like "[^\ ']+"
                #
                ('/proj/port_ots/[^/]+/Python-{pyver}\.[^/]+/', 'ots/'),
                ('/proj/port_ots/[^/]+/Python-{pyver}\.[^/ \n\'"]+', 'ots'),

                ('/proj/port_ots/[^/]+/readline-6.3\.[^/]+/', 'ots/'),
                ('/proj/port_ots/[^/]+/gsl-2.3\.[^/]+/', 'ots/'),

                ('/proj/port_ots/[^/]+/', 'ots/'),
                ('/proj/port_ots/[^/ \n\'"]+', 'ots'),

                ('/proj/xena/ciao[^/]+/[^/]+/ciao[^/]+/', 'ots/'),
                ('/proj/xena/ciao[^/]+/[^/]+/ciao[^/ \n\'"]+', 'ots'),  # do I need this?

                ('/proj/xena/ciaot_build/[^/]+/ciao_\d\d\d\d/[^/]+/ciao[^/]+/', 'ots/'),
            ]]


big_table = make_big_table('Linux64')


def convert_line(orig):
    """Replace hard-coded build paths in the input.

    Very specialized, and not very general. Does not strip the
    line to try and keep spacing to match the original.
    The assumption is that there are no spaces in the paths
    being replaced.
    """

    for k, v in big_table:
        orig = k.sub(v, orig)

    return orig


def check_backup_name(filename):
    """If filename exists, update it by adding on numbers
    until it doesn't exist, starting at 2.

    This assumes the name does not match a "non-file" type,
    such as a directory or pipe.
    """

    if not os.path.isfile(filename):
        return filename

    n = 2
    while True:
        testfile = "{}{}".format(filename, n)
        if not os.path.isfile(testfile):
            return testfile

        n += 1


# TODO: can consolidate a lot of the following

def update_sysconfigdata():
    """Rewrite _sysconfigdata.py to _sysconfigdata.py.org[n]

    n is 2 or greater (and is used if .org or .org[n-1] exists).
    """

    # I assume this is valid, but is there a better way to do it?
    pyver = 'python{}.{}'.format(sys.version_info.major,
                                 sys.version_info.minor)

    name = "_sysconfigdata.py"
    infile = os.path.join(ascds_install, 'ots', 'lib', pyver, name)
    if not os.path.isfile(infile):
        raise IOError("Unable to find {}".format(infile))

    backupfile = infile + ".org"

    if hack_filenames:
        backupfile = os.path.basename(backupfile)

    # Add any counter on as needed
    backupfile = check_backup_name(backupfile)

    # write out the backup file, then overwrite the input
    store = []
    with open(infile, 'r') as ifh:
        with open(backupfile, 'w') as ofh:
            for l in ifh.readlines():
                # do not strip to keep the spacing
                ofh.write(l)

                store.append(convert_line(l))

    print("Created: {}".format(backupfile))

    # Only write out the converted data once the backup has been fully
    # written out.
    #
    if hack_filenames:
        infile = os.path.basename(infile)

    with open(infile, 'w') as ofh:
        for l in store:
            ofh.write(l)

    print("Overwrote: {}".format(infile))


def update_python_makefile():
    """I had hoped that only _sysconfigdata.py needed editing,
    but apparently not.
    """

    v = '{}.{}'.format(sys.version_info.major,
                       sys.version_info.minor)

    infile = os.path.join(ascds_install, 'ots', 'lib',
                          'python{}'.format(v), 'config-{}m'.format(v),
                          'Makefile')

    if not os.path.isfile(infile):
        raise IOError("Unable to find {}".format(infile))

    backupfile = infile + ".org"

    if hack_filenames:
        backupfile = os.path.basename(backupfile)

    # Add any counter on as needed
    backupfile = check_backup_name(backupfile)

    # write out the backup file, then overwrite the input
    store = []
    with open(infile, 'r') as ifh:
        with open(backupfile, 'w') as ofh:
            for l in ifh.readlines():
                # do not strip to keep the spacing
                ofh.write(l)

                store.append(convert_line(l))

    print("Created: {}".format(backupfile))

    # Only write out the converted data once the backup has been fully
    # written out.
    #
    if hack_filenames:
        infile = os.path.basename(infile)

    with open(infile, 'w') as ofh:
        for l in store:
            ofh.write(l)

    print("Overwrote: {}".format(infile))


def update_pc(infile):
    """Update pc file if it needs to be."""

    orig_store = []
    store = []
    same = True
    with open(infile, 'r') as ifh:
        for orig in ifh.readlines():
            new = convert_line(orig)
            orig_store.append(orig)
            store.append(new)
            same &= (new == orig)

    if same:
        return

    if hack_filenames:
        infile = os.path.basename(infile)

    origfile = check_backup_name(infile + ".org")
    with open(origfile, 'w') as ofh:
        for l in store:
            ofh.write(l)

    print("Created: {}".format(origfile))

    with open(infile, 'w') as ofh:
        for l in store:
            ofh.write(l)

    print("Overwrote: {}".format(infile))


def update_pc_files():
    """Update pkg-config files. Easiest to process them all
    and only change those that need changing, rather than hard-code
    a list of problem files.
    """

    pat1 = os.path.join(ascds_install, 'lib', 'pkgconfig', '*pc')
    matches1 = glob.glob(pat1)
    if len(matches1) == 0:
        raise IOError("No matches for {}".format(pat1))

    pat2 = os.path.join(ascds_install, 'ots', 'lib', 'pkgconfig', '*pc')
    matches2 = glob.glob(pat2)
    if len(matches2) == 0:
        raise IOError("No matches for {}".format(pat2))

    for pcfile in matches1 + matches2:
        update_pc(pcfile)


if __name__ == "__main__":

    nargs = len(sys.argv)
    if nargs > 2 or (nargs == 2 and sys.argv[1] != "hack"):
        sys.stderr.write("Usage: {} [hack]\n".format(sys.argv[0]))
        sys.exit(1)

    hack_filenames = nargs == 2

    print("Updating CIAO in {}".format(ascds_install))
    update_sysconfigdata()
    update_python_makefile()
    update_pc_files()
