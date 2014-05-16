# member.mixins
# Authentication Mixins
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 15:40:50 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: mixins.py [] benjamin@bengfort.com $

"""
Authentication Mixins
"""

##########################################################################
## Imports
##########################################################################

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

##########################################################################
## Mixins
##########################################################################

class LoginRequired(object):
    """
    Ensures that user must be authenticated in order to access view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)
