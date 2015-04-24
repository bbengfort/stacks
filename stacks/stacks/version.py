# stacks.version
# Helper module for Stacks version information
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 20:02:50 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: version.py [] benjamin@bengfort.com $

"""
Helper module for Stacks version information
"""

##########################################################################
## Versioning
##########################################################################

__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 0,
}


def get_version(short=False):
    """
    Returns the version from the version info.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))
    return ''.join(vers)
