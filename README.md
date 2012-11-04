sorl-defined-thumbnails
=======================

This is a plugin over standard sorl-thumbnails that constrains your thumbnail creation to only a set of pre defined sizes.

Define your thumbnail sizes in your settings:

    SORL_DEFINED_THUMBNAILS = {
        'small_cropped': {
            'size': (50, 50),
            'options': {
                'crop': 'center'
            }
        },
        'small': {
            'size': (50, 50),
        },
        'medium': {
            'size': (350, 350),
        },
    }


Add to your `INSTALLED_APPS` **before** `sorl.thumbnail`

    INSTALLED_APPS = (
        'defined_thumbnails',
        'sorl.thumbnail',
    )

This is important so the `{% thumbnail %}` template tag gets overriden by the new one.

Usage
-----

In your templates now do:

    {% load thumbnail %}

    {% block content %}
        {% thumbnail object.pic_field "medium" as thumb %}
        <img src="{{thumb.url}}"/>
    {% endthumbnail %}

    {% endblock %}


Migration
---------

By default, the new template tag will allow you to continue using old geometries not defined in `SORL_DEFINED_THUMBNAILS`.
If you want to raise errors with this, set `SORL_DEFINED_STRICT` to `True`.


Finding all templates to convert
--------------------------------

This app comes with a management command that will look in all app dirs and template dirs for matches of the thumbnail tag.

    ./manage.py find_thumbnail_tags

It will print all usages of the `{% thumbnail %}` tag in your templates
