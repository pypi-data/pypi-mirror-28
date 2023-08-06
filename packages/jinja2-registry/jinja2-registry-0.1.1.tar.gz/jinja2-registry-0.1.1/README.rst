jinja2_registry
***************

.. image:: https://img.shields.io/travis/3ptscience/jinja2-registry.svg
    :target: https://travis-ci.org/3ptscience/jinja2-registry

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: https://github.com/3ptscience/jinja2-registry/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/jinja2-registry.svg
    :target: https://pypi.python.org/pypi/jinja2-registry

.. image:: https://img.shields.io/pypi/pyversions/jinja2-registry.svg
    :target: https://pypi.python.org/pypi/jinja2-registry


**jinja2_registry** is a convenience library for managing multiple template namespaces with Jinja2

Example
*******

The following Python code sets up a ``jinja2.Environment`` and three distinct ``jinja2.FileSystemLoader`` objects under a ``jinja2.PrefixLoader``. It then renders a HTML page based on ``title.html`` that includes several other files.

.. code:: python

    from jinja2_registry import Renderer, register_filesystem_loader

    register_filesystem_loader('layouts', 'templates/layouts')
    register_filesystem_loader('partials', 'templates/partials')
    register_filesystem_loader('pages', 'templates/pages')

    renderer = Renderer('pages/title.html')
    html = renderer.render()
    print(html)

The result is rendered from 4 HTML templates, which are located in different directories. In this example, all of the templates are read from the filesystem; however, users may make use of ``register_loader`` to attach any standard Jinja2 loader to the registry.

**Result**

.. code:: html

    <!DOCTYPE html>
    <html>
      <head>
        <title>new_title</title>
      </head>
      <body>
        <ul>
          <li><a href="/content">Content page</a></li>
          <li><a href="/title">New title page</a></li>
        </ul>
        <div>
          <p>some_content</p>
        </div>
      </body>
    </html>

----

The HTML templates are organized into the following structure. Layouts are separated from partials and content. In a production deployment, layouts would likely be stored separately from pages (e.g., in a library), and partials might be automatically generated.

**File structure**::

    templates/
    ├── layouts
    │   └── base.html
    ├── pages
    │   ├── content.html
    │   └── title.html
    └── partials
        └── nav.html

**templates/layouts/base.html**

.. code:: html

    <!DOCTYPE html>
    <html>
      <head>
        <title>{% block title %}default_title{% endblock %}</title>
      </head>
      <body>
        {% include "partials/nav.html" %}
        <div>
          {% block content %}{% endblock %}
        </div>
      </body>
    </html>

**templates/partials/nav.html**

.. code:: html

    <ul>
      <li><a href="/content">Content page</a></li>
      <li><a href="/title">New title page</a></li>
    </ul>

**templates/pages/content.html**

.. code:: html

    {% extends "layouts/base.html" %}
    {% block content %}
          <p>some_content</p>
    {%- endblock %}

**templates/pages/title.html**

.. code:: html

    {% extends "pages/content.html" %}
    {% block title %}new_title{% endblock %}
