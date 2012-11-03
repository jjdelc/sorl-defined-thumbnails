# coding: utf-8

from django.template import Library

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode, logger, TemplateSyntaxError

from defined_thumbnails import helpers


register = Library()

class DefinedThumbnailNode(ThumbnailNode):

    def __init__(self, parser, token):
        super(DefinedThumbnailNode, self).__init__(parser, context)
        if helpers.is_valid_geometry(self.geometry):
            self.geometry = helpers.convert_to_geometry(self.geometry)
        else:
            raise TemplateSyntaxError(u'Invalid thumbnail size "%s"' % self.geometry)

    def _render(self, context):
        return super(DefinedThumbnailNode, self)._render(context)



@register.tag
def thumbnail(parser, token):
    if helpers.is_enabled():
        return ThumbnailNode(parser, token)
    return DefinedThumbnailNode(parser, token)
