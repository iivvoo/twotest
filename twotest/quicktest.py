"""
Source: http://datadesk.latimes.com/posts/2012/06/test-your-django-app-with-travisci/
Slightly modified by Nicolas Kuttler.
"""

import os
import sys

from django.conf import settings


class QuickDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.

    Example usage:

        >>> QuickDjangoTest('app1', 'app2')

    Based on a script published by Lukasz Dziedzia at:
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    )
    WEBMASTER_VERIFICATION = {}

    def __init__(self, apps, installed_apps=(), *args, **kwargs):
        self.test_apps = apps
        self.installed_apps = installed_apps
        self.settings = kwargs
        self._tests()

    def _tests(self):
        """
        Fire up the Django test suite developed for version 1.2
        """
        default_settings = dict(
            DEBUG = True,
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'memory:///',
                }
            },
            INSTALLED_APPS = self.INSTALLED_APPS + tuple(self.installed_apps),
            TEMPLATE_DIRS = (
                # './test_project/templates/',
            ),
            STATIC_URL='/static',
            SITE_ID=1,
            ROOT_URLCONF="twotest.emptyurls",
        )
        default_settings.update(self.settings)
        settings.configure(
            **default_settings
        )
        import pytest
        for app in self.test_apps:
            failures = pytest.main(["--tb=short", app])
            if failures:
                sys.exit(failures)


if __name__ == '__main__':
    """
    What do when the user hits this file from the shell.

    Example usage:

        $ python quicktest.py app1 app2

    """
    import argparse
    parser = argparse.ArgumentParser(
        usage="[args]",
        description="Run Django tests on the provided applications."
    )
    parser.add_argument('apps', nargs='+', type=str)
    options = parser.parse_args()
    QuickDjangoTest(options.apps)
