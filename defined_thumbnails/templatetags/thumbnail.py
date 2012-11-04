# coding: utf-8

from django.template import Library

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode, logger, TemplateSyntaxError

from defined_thumbnails import helpers


register = Library()

USE_STRICT = helpers.use_strict()
IS_ENABLED = helpers.is_enabled()

class DefinedThumbnailNode(ThumbnailNode):

    def __init__(self, parser, token):
        super(DefinedThumbnailNode, self).__init__(parser, token)
        if helpers.is_valid_geometry(self.geometry):
            geom_name = helpers.get_geom_name(self.geometry)
            geom_str = helpers.get_geom_string(geom_name)
            geom_opts = helpers.get_geom_opts(geom_name)

            self.geometry = parser.compile_filter(geom_str)
            self.options = [(k, parser.compile_filter(v)) for k, v in geom_opts]
        else:
            if USE_STRICT:
                logger.warning(u'Invalid geometry: %s' % self.geometry)
                raise TemplateSyntaxError(
                    u'Invalid thumbnail size %s' % self.geometry)


@register.tag
def thumbnail(parser, token):
    if IS_ENABLED:
        return DefinedThumbnailNode(parser, token)
    return ThumbnailNode(parser, token)
