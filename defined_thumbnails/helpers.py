# coding: utf-8

from django.conf import settings

def is_enabled():
    """
    Checks if the appropriate settings for pre defined thumbnails are set.
    If they aren't then just continue with regular sorl-thumbnail
    """
    return hasattr(settings, 'SORL_DEFINED_THUMBNAILS')


def clean_geom(geom):
    return str(geom).strip('"').lower()


def is_valid_geometry(geom):
    """
    A geometry is valid if it fits within the pre defined thumbnail sizes.
    """
    named_sizes = get_named_sizes()
    defined_sizes = get_defined_sizes()
    return clean_geom(geom) in named_sizes + defined_sizes


def is_valid_opts(opts):
    if len(opts) != len(settings.SORL_DEFINED_THUMBNAILS):
        return False

    # TODO: Make sure all opts match
    return True


def is_valid_geometry_and_opts(geom, opts):
    return is_valid_geometry(geom) and is_valid_opts(opts)


def get_named_sizes():
    defined_sizes = settings.SORL_DEFINED_THUMBNAILS
    return defined_sizes.keys()


def size_to_str(size_tup):
    return '%sx%s' % size_tup


def get_defined_sizes():
    defined_sizes = settings.SORL_DEFINED_THUMBNAILS
    return [size_to_str(v['size']) for v in defined_sizes.values()]


def get_thumb_data(geom):
    return settings.SORL_DEFINED_THUMBNAILS[clean_geom(geom)]


def get_thumb_name_from_size_str(geom):
    for tname, tdata in settings.SORL_DEFINED_THUMBNAILS.items():
        if tdata['size'] == geom:
            return tname


def get_geom_name(geom):
    cgeom = clean_geom(geom)
    if cgeom in get_defined_sizes():
        name = get_thumb_name_from_size_str(cgeom)
    else:
        name = cgeom
    return name


def get_geom_string(geom):
    thumb = get_thumb_data(geom)
    return '"%s"' % size_to_str(thumb['size'])


def get_geom_opts(geom):
    thumb = get_thumb_data(geom)
    return [(k, '"%s"' % v) for k, v in thumb['options'].items()]


def use_strict():
    return getattr(settings, 'SORL_DEFINED_STRICT', False)

