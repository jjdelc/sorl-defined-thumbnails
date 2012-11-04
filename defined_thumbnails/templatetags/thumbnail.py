# coding: utf-8

from django.template import Library

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode, logger, TemplateSyntaxError

from defined_thumbnails import helpers


register = Library()

USE_STRICT = helpers.use_strict()

class DefinedThumbnailNode(ThumbnailNode):

    def __init__(self, parser, token):
        super(DefinedThumbnailNode, self).__init__(parser, token)
        if helpers.is_valid_geometry(self.geometry):
            new_geom = helpers.convert_to_geometry(self.geometry)
            self.geometry = parser.compile_filter(new_geom)
        else:
            if USE_STRICT:
                logger.warning(u'Invalid geometry: %s' % self.geometry)
                raise TemplateSyntaxError(
                    u'Invalid thumbnail size %s' % self.geometry)

    def _render(self, context):
        return super(DefinedThumbnailNode, self)._render(context)


@register.tag
def thumbnail(parser, token):
    if helpers.is_enabled():
        return DefinedThumbnailNode(parser, token)
    return ThumbnailNode(parser, token)
