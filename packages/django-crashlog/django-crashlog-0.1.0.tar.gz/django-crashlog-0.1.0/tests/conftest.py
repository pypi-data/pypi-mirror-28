import os

import sys

import pytest

from crashlog.models import Error


def pytest_configure(config):

    import warnings
    warnings.simplefilter('once', DeprecationWarning)
    HERE = os.path.join(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(HERE, 'demo'))



@pytest.fixture()
def error(db):
    return Error.objects.create(class_name='PermissionDenied',
                         message='Error Message',
                         traceback='',
                         url='/',
                         server_name='',
                         )
