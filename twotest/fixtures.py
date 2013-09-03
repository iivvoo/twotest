"""
    client funcargs for py.test / django. Based on django_pytest
"""

from django.conf import settings
from django.test.client import Client
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command
from django.core import mail

import pytest

@pytest.fixture
def django_client(request):
    """
        Setup / destroy testing database.
        Additionally, set the MEDIA_ROOT to the TEST_MEDIA_ROOT and clean up
        afterwards. This gives a cleaner fixture, and avoids testimages ending up
        in the MEDIA_ROOT folder.

        Of course we need to make sure we don't clean up a real MEDIA_ROOT. So
        only clean up the explicit TEST_MEDIA_ROOT, and only if it's different
        from the real MEDIA_ROOT
    """
    old_name = getattr(settings, 'DATABASE_NAME', 'default')

    def test_media_root():
        return getattr(settings, "TEST_MEDIA_ROOT", settings.MEDIA_ROOT)

    def setup():
        setup_test_environment()
        if not hasattr(settings, 'DEBUG'):
            settings.DEBUG = False
        from django.db import connection
        if 'south' in settings.INSTALLED_APPS:
            try:
                from south.management.commands import patch_for_test_db_setup
                patch_for_test_db_setup()
            except ImportError:
                pass
        connection.creation.create_test_db(verbosity=0, autoclobber=True)
        # call_command("migrate", database=connection.alias)
        c = Client()
        c.orig_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = test_media_root()
        return c

    def teardown(client):
        teardown_test_environment()
        from django.db import connection
        connection.creation.destroy_test_db(old_name, verbosity=False)

    return request.cached_setup(setup, teardown, "session")

@pytest.fixture
def client(request):
    """ as django_client, but also flushes the database """
    def cleanup_media():
        return getattr(settings, "CLEANUP_MEDIA", False)

    def setup():
        return request.getfuncargvalue('django_client')

    def teardown(client):
        call_command('flush', verbosity=0, interactive=False)
        mail.outbox = []
        import shutil
        if cleanup_media() and settings.MEDIA_ROOT != client.orig_media_root:
            try:
                shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
            except OSError:
                pass

    return request.cached_setup(setup, teardown, "function")


