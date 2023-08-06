import os
from fnmatch import fnmatchcase

from distutils import log
from distutils.util import convert_path

from .datafiles import ManifestInRewriter


# This function:
#   Source: http://svn.pythonpaste.org/Paste/trunk/paste/util/finddata.py
#    (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
#   Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
#
#  Provided as an attribute, so you can append to these instead of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
#
def find_package_data(
        where='.', package='',
        exclude=standard_exclude,
        exclude_directories=standard_exclude_directories,
        only_in_packages=True,
        show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if fnmatchcase(name, pattern) or fn.lower() == pattern.lower():
                        bad_name = True
                        if show_ignored:
                            log.warn("Directory %s ignored by pattern %s" % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, '__init__.py'))
                    and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if fnmatchcase(name, pattern) or fn.lower() == pattern.lower():
                        bad_name = True
                        if show_ignored:
                            log.warn("File %s ignored by pattern %s" % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out


# TODO: where does this fit in?
# TODO: take a ManifestInRewriter and work on it, don't rewrite yourself
def rewrite_manifest_in_from_package_data_etc(package_data, output_file="MANIFEST.in", extra_include=None):
    """Since package_data is a big fat lie (see below), use this to rewrite MANIFEST.in based on a package_data dictionary.
    See: http://blog.codekills.net/2011/07/15/lies,-more-lies-and-python-packaging-documentation-on--package_data-/

    To allow re-running this function, it leaves an auto-generation signature in the output, to be detected and replaced.
    """
    rewriter = ManifestInRewriter(output_file)
    for (package_path, files_included) in package_data.items():
        # TODO: we may want to support packages that are in a subdirectory somewhere
        for file_included in files_included:
            fullpath = os.path.join(os.path.sep.join(package_path.split(".")), file_included)
            posix_fullpath = fullpath.replace(os.path.sep, "/")
            rewriter.add_include(posix_fullpath)
    if extra_include:
        for record in extra_include:
            if isinstance(record, basestring):
                # strings are to be included
                rewriter.add_include(record)
            else:
                # two-tuples are to be recursive included
                (directory, glob_pattern) = record
                rewriter.add_recursive_include(directory, glob_pattern)
    rewriter.rewrite()
