# coding: utf-8

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode, logger, TemplateSyntaxError, safe_filter
from sorl.thumbnail.templatetags.thumbnail import margin as sorl_margin
from sorl.thumbnail.templatetags.thumbnail import is_portrait as sorl_is_portrait
from defined_thumbnails import helpers

from django.template import Library


register = Library()

USE_STRICT = helpers.use_strict()
IS_ENABLED = helpers.is_enabled()
ALLOW_OPTIONS = helpers.allow_options()


class DefinedThumbnailNode(ThumbnailNode):

    def __init__(self, parser, token, use_strict=USE_STRICT):
        super(DefinedThumbnailNode, self).__init__(parser, token)
        if helpers.is_valid_geometry_and_opts(self.geometry, self.options):
            geom_name = helpers.get_geom_name(self.geometry)
            geom_str = helpers.get_geom_string(geom_name)
            geom_opts = helpers.get_geom_opts(geom_name)

            self.geometry = parser.compile_filter(geom_str)
            base_options = self.options or []
            self.options = base_options + [(k, parser.compile_filter(v)) for k, v in geom_opts]
        else:
            msg = helpers.get_invalid_msg(self.geometry, self.options)
            if use_strict:
                logger.warning(msg)
                raise TemplateSyntaxError(msg)


@register.tag
def thumbnail(parser, token):
    if IS_ENABLED:
        return DefinedThumbnailNode(parser, token, use_strict=USE_STRICT)
    return ThumbnailNode(parser, token)


@register.tag
def dthumbnail(parser, token):
    return DefinedThumbnailNode(parser, token, use_strict=True)


@safe_filter(error_output='auto')
@register.filter
def margin(file_, geom_string):
    if IS_ENABLED and geom_string in helpers.get_named_sizes():
        geom_string = helpers.clean_geom(helpers.get_geom_string(geom_string))
    return sorl_margin(file_, geom_string)


@safe_filter(error_output=False)
@register.filter
def is_portrait(file_):
    return sorl_is_portrait(file_)
