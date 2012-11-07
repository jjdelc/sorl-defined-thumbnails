# coding: utf-8

from django.template import Library

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode, logger, TemplateSyntaxError

from defined_thumbnails import helpers


register = Library()

USE_STRICT = helpers.use_strict()
IS_ENABLED = helpers.is_enabled()

class DefinedThumbnailNode(ThumbnailNode):

    def __init__(self, parser, token, use_strict=USE_STRICT):
        super(DefinedThumbnailNode, self).__init__(parser, token)
        if helpers.is_valid_geometry_and_opts(self.geometry, self.options):
            geom_name = helpers.get_geom_name(self.geometry)
            geom_str = helpers.get_geom_string(geom_name)
            geom_opts = helpers.get_geom_opts(geom_name)

            self.geometry = parser.compile_filter(geom_str)
            self.options = [(k, parser.compile_filter(v)) for k, v in geom_opts]
        else:
            msg = helpers.get_invalid_msg(self.geometry, self.options)
            logger.warning(msg)
            if use_strict:
                raise TemplateSyntaxError(msg)


@register.tag
def thumbnail(parser, token):
    if IS_ENABLED:
        return DefinedThumbnailNode(parser, token, use_strict=USE_STRICT)
    return ThumbnailNode(parser, token)


@register.tag
def dthumbnail(parser, token):
    return DefinedThumbnailNode(parser, token, use_strict=True)
