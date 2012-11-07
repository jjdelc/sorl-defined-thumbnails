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
        'medium_cropped': {
            'size': (350, 350),
            'options': {
                'crop': 'center'
            }
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

This app provides two template tags `{% dthumbnail %}` and overrides the standard `{% thumbnail %}` so it now takes the named thumbnails instead of arbitrary arguments.

In your templates now do:

    {% load thumbnail %}

    {% block content %}
        {% thumbnail object.pic_field "medium" as thumb %}
        <img src="{{thumb.url}}"/>
    {% endthumbnail %}

    {% endblock %}

You can also keep using the standard syntax:

    {% thumbnail object.pic_field "350x350" crop="center "as thumb %}

as long as the parameters entered match any of the defined sizes.

When using strict mode the template tags will raise a syntax error if the parameters don't match the named thumbnails, otherwise they will only get logged.

Alternatively you can use the `{% dthumbnail %}` tag which works like the overriden `{% thumbnail %}` tag but will always be strict. This tag also takes `{% empty %}` and closes with `{% endthumbnail %}`.

Migration
---------

By default, the new template tag will allow you to continue using old geometries not defined in `SORL_DEFINED_THUMBNAILS`.
If you want to raise errors with this, set `SORL_DEFINED_STRICT` to `True`.

Finding all template occurences
-------------------------------

    ./manage.py thumbnail_tags find_bad

Will show all the occurences of the `{% thumbnail %}` tag in your templates.


Finding all templates to convert
--------------------------------

This app comes with a management command that will look in all app dirs and template dirs for matches of the thumbnail tag.

    ./manage.py thumbnail_tags find_bad

It will print all usages of the `{% thumbnail %}` tag in your templates


Suggest which sizes to define
-----------------------------

    ./manage.py thumbnail_tags suggest_sizes

Will run a tally of all the `{% thumbnail %}` tags found in your templates and show you the occurences for each combination of geometry/options.

This should help you find which sizes to create in order to make the least changes in your templates.
