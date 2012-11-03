# coding: utf-8

from django.conf import settings

def is_enabled():
    """
    Checks if the appropriate settings for pre defined thumbnails are set.
    If they aren't then just continue with regular sorl-thumbnail
    """
    return hasattr(settings, 'SORL_DEFINED_THUMBNAILS')


def is_valid_geometry(geom):
    """
    A geometry is valid if it fits within the pre defined thumbnail sizes.
    """
    named_sizes = get_named_sizes()
    defined_sizes = get_defined_sizes()
    if use_strict():
        return geom in named_sizes + defined_sizes
    return geom


def get_named_sizes():
    defined_sizes = settings.SORL_DEFINED_THUMBNAILS
    return defined_sizes.keys()


def get_defined_sizes():
    defined_sizes = settings.SORL_DEFINED_THUMBNAILS
    return defined_sizes.values()


def convert_to_geometry(geom):
    if geom in get_defined_sizes():
        return geom

    return get_named_sizes()[geom]

def use_strict():
    return getattr(settings, 'SORL_DEFINED_STRICT', False)