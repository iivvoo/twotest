from django.core.management.base import BaseCommand
import pytest
import optparse

from django.conf import settings

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option('-s',
            action='store_false',
            dest='capture',
            default=True,
            help='Capture output'),
        optparse.make_option('-k',
            dest='keyword',
            default='',
            help='Limit by keyword'),
        )

    def handle(self, *a, **b):
        ## http://pytest.org/latest/usage.html
        ## --tb=native is also usable
        opts = ["--tb=short", "--pastebin=all"]

        settings.DATABASES = dict(default=settings.TEST_DB)
        if not b.get('capture'):
            opts.append("-s")
        if b.get('keyword') and b['keyword']:
            opts.append("-k")
            opts.append(b['keyword'])

        pytest.main(opts + list(a))

