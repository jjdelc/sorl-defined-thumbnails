# coding: utf-8

from django.core.management.base import BaseCommand


def make_line_data(num, line, filename):
    return {
        'line': line,
        'number': num,
        'file': filename,
    }


def has_thumbnail_tag(line):
    return 'thumbnail' in line


def tlines_in_file(template_file):
    lines = []
    for num, line in open(template_file):
        if has_thumbnail_tag(line):
            lines.append(make_line_data(num, line, template_file))

    return lines


def thumbnail_lines():
    """
    """
    tlines = []
    for tfile in template_files():
        tlines.extend(tlines_in_file(tfile))
    return tlines


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print '\n'.join(thumbnail_lines())
