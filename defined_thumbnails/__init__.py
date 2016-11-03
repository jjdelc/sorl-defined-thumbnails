# coding: utf-8

from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail

from defined_thumbnails import helpers


def get_thumbnail(file_, geometry_string, **options):
    if helpers.is_valid_geometry(geometry_string):
        geom_opts = dict(helpers.clean_opts(
            helpers.get_geom_opts(geometry_string)))
        geometry_string = helpers.clean_geom(
            helpers.get_geom_string(geometry_string))
        options.update(geom_opts)
    return sorl_get_thumbnail(file_, geometry_string, **options)