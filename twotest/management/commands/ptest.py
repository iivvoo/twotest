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
        optparse.make_option('-p',
            action='store_false',
            dest='paste',
            default=True,
            help='Paste result to pastebin'),
        )

    def handle(self, *a, **b):
        ## http://pytest.org/latest/usage.html
        ## --tb=native is also usable
        opts = ["--tb=short"]

        settings.DATABASES = dict(default=settings.TEST_DB)
        if not b.get('capture'):
            opts.append("-s")
        if b.get('keyword') and b['keyword']:
            opts.append("-k")
            opts.append(b['keyword'])
        if not b.get('paste'):
            opts.append("--pastebin=all")

        pytest.main(opts + list(a))

