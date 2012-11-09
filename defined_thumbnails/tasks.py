# coding: utf-8


from django.conf import settings

from sorl.thumbnail import get_thumbnail

from defined_thumbnails import helpers


def get_thumbnail_sizes():
    return settings.SORL_DEFINED_THUMBNAILS.values()

def generate_all_thumbs(img_field):
    optimized_get_thumbnail(img_field, get_thumbnail_sizes())

def optimized_get_thumbnail(file_, all_sizes):
    """
    This function is based on:
        `sorl.thumbnail.base.ThumbnailBackend.get_thumbnail`

    but optimized to download the image file only once from the backend
    and generate all thumbnails in memory.

    If we called .get_thumbnail() for each size, we would do a separate
    download for each rendering which takes too long.

    We are not checking if the image is cached. Always generate
    the thumb in this call.
    We also assume that the thumbnail does not exist for overwriting
    """
    from sorl.thumbnail.images import ImageFile
    from sorl.thumbnail import default

    backend = default.backend
    source = ImageFile(file_)
    # Here we call .get_image() once, we'll use this for all thumbs
    source_image = default.engine.get_image(source)

    for thumb_opts in all_sizes:
        geometry_string = helpers.size_to_str(thumb_opts['size'])
        # .copy() opts so settings doesn't get updated!!
        options = thumb_opts.get('options', {}).copy()
        for key, value in backend.default_options.iteritems():
            options.setdefault(key, value)
        name = backend._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = ImageFile(name, default.storage)
        size = default.engine.get_image_size(source_image)
        source.set_size(size)
        backend._create_thumbnail(source_image, geometry_string, options,
            thumbnail)
        default.kvstore.get_or_set(source)
        default.kvstore.set(thumbnail, source)
