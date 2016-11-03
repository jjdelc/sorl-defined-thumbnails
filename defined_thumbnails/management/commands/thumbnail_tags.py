# coding: utf-8
from __future__ import print_function

import os
import re
from collections import defaultdict

from django.conf import settings
from django.template.loaders import app_directories
from django.core.management.base import BaseCommand, CommandError

from sorl.thumbnail.templatetags.thumbnail import kw_pat

from defined_thumbnails import helpers


TTAG_RE = re.compile('{%\ *thumbnail .*?%}')


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


def find_all():
    out = []
    for tline in thumbnail_lines():
        out.append(convert_to_txt(tline).encode('utf-8'))
    return out


def template_doesnt_match(template_line):
    tags_present = extract_present_tags(template_line)
    return not all(tag_is_ok(tag) for tag in tags_present)

def extract_present_tags(template_line):
    return TTAG_RE.findall(template_line['line'])


def tag_is_ok(tag_string):
    geom = geom_from_tag(tag_string)
    opts = opts_from_tag(tag_string)
    return helpers.is_valid_geometry_and_opts(geom, opts)

def geom_from_tag(tag_string):
    return helpers.clean_geom(tag_chunks(tag_string)[0])

def tag_chunks(tag):
    tag = tag.strip('}')
    tag = tag.strip('{')
    tag = tag.strip('%')
    tag = tag.strip()
    tag = tag.lstrip('thumbnail')
    tag = tag.strip()
    return tag.split()[1:-2]


def opts_from_tag(tag_string):
    chunks = tag_chunks(tag_string)[1:]
    opts = []
    for pat in chunks:
        match = kw_pat.match(pat)
        key = match.group('key')
        val = match.group('value')
        opts.append((key, val))

    opts.sort(key=lambda x: x[0]) # Make sure they are always in the same order
    return opts


def find_bad():
    out = []
    for template_line in thumbnail_lines():
        if template_doesnt_match(template_line):
            out.append(convert_to_txt(template_line).encode('utf-8'))

    return out


def suggested_sizes():
    tally = defaultdict(int)
    for template_line in thumbnail_lines():
        for tag in extract_present_tags(template_line):
            normal_tag = normalize_tag(tag)
            tally[normal_tag] += 1
    return tally


def normalize_tag(tag):
    return u'{%% thumbnail img %s %%}' % ' '.join(tag_chunks(tag))


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not args:
            return self.bad_command()

        command = args[0]

        if command == 'suggest_sizes':
            return self.suggest_sizes()
        elif command == 'list':
            out = find_all()
        elif command == 'find_bad':
            out = find_bad()
        else:
            return self.bad_command()

        if not out:
            print('No results found')

        print(u'\n'.join(out))

    def bad_command(self):
        raise CommandError('Invalid command')

    def suggest_sizes(self):
        out = []
        for tag, count in suggested_sizes().items():
            out.append((count, tag))

        out.sort(key=lambda x: x[0])
        print('\n'.join('%3d: %s' % (count, tag) for count, tag in out))
