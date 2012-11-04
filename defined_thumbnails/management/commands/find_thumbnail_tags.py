# coding: utf-8

import os
import re

from django.conf import settings
from django.template.loaders import app_directories
from django.core.management.base import BaseCommand


TTAG_RE = re.compile('{%\ *thumbnail')


def make_line_data(num, line, filename):
    return {
        'line': line,
        'number': num,
        'file': filename,
    }


def has_thumbnail_tag(line):
    return TTAG_RE.match(line)


def tlines_in_file(template_file):
    lines = []
    for num, line in enumerate(open(template_file), 1):
        if has_thumbnail_tag(line):
            lines.append(make_line_data(num, line, template_file))

    return lines


def template_files():
    """
    Returns a list of all template files full path
    """
    complete_files = []
    all_dirs = list(settings.TEMPLATE_DIRS) + list(app_directories.app_template_dirs)
    for tdir in all_dirs:
        for path, dirs, files in os.walk(tdir):
            for fname in files:
                complete_files.append(os.path.realpath(
                    os.path.join(path, fname)))

    return complete_files


def thumbnail_lines():
    """
    """
    tlines = []
    for tfile in template_files():
        tlines.extend(tlines_in_file(tfile))
    return tlines


def convert_to_txt(tline):
    return u'%s:%s\n\t%s' % (tline['file'], tline['number'], tline['line'])


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        out = []
        for tline in thumbnail_lines():
            out.append(convert_to_txt(tline).encode('utf-8'))
        print u'\n'.join(out)
