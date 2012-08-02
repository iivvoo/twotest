"""
    client funcargs for py.test / django. Based on django_pytest
"""

from django.conf import settings
from django.test.client import Client
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command
from django.core import mail

def pytest_funcarg__django_client(request):
    """
        Setup / destroy testing database
    """
    old_name = getattr(settings, 'DATABASE_NAME', 'default')
    def setup():
        setup_test_environment()
        if not hasattr(settings, 'DEBUG'):
            settings.DEBUG = False
        from django.db import connection
        connection.creation.create_test_db(verbosity=0, autoclobber=True)
        return Client()

    def teardown(client):
        teardown_test_environment()
        from django.db import connection
        connection.creation.destroy_test_db(old_name, verbosity=False)

    return request.cached_setup(setup, teardown, "session")

def pytest_funcarg__client(request):
    """ as django_client, but also flushes the database """
    def setup():
        return request.getfuncargvalue('django_client')

    def teardown(client):
        call_command('flush', verbosity=0, interactive=False)
        mail.outbox = []

    return request.cached_setup(setup, teardown, "function")


