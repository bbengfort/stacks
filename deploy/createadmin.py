#!/usr/bin/env python
"""
Python script to create a temporary admin account if no user accounts have
been created on the server (allowing access to the admin).
"""

# Imports
import os
import sys

# Fix the path
project = os.path.abspath(os.path.join(os.path.dirname(__file__), '../stacks/'))
sys.path.append(project)

# Import Django
from django.contrib.auth.models import User

# Main Statement
def main(*uargs):
    if User.objects.count() == 0:
        admin = User.objects.create_user(*uargs)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        return True
    return False

if __name__ == '__main__':
    main('benjamin', 'benjamin@bengfort.com', 'password')
