sorl-defined-thumbnails
=======================

This is a plugin over standard sorl-thumbnails that constrains your thumbnail creation to only a set of pre defined sizes.

Define your thumbnail sizes in your settings:


    SORL_DEFINED_THUMBNAILS = {
        'small': '50x50'
        'medium': '250x250'
        'large': '800x800'
    }


Add to your `INSTALLED_APPS` **AFTER** `sorl.thumbnail`

    INSTALLED_APPS = (
        'sorl.thumbnail',
        'defined_thumbnails',
    )

This is important so the `{% thumbnail %}` template tag gets overriden by the new one.

Usage
-----

In your templates now do:

    {% load thumbnail %}
    {% block content %}
    {% thumbnail medium as thumb %}
    <img src="{{thumb.url}}"/>
    {% endthumbnail %}
    {% endblock %}


Migration
---------

By default, the new template tag will allow you to continue using old geometries not defined in `SORL_DEFINED_THUMBNAILS`.
If you want to raise errors with this, set `SORL_DEFINED_STRICT` to `True`.
