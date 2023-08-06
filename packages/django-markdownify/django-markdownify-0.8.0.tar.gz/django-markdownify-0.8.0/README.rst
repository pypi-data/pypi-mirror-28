Django Markdownify - A Django Markdown filter
=============================================
**Django Markdownify is a template filter to convert Markdown to HTML in Django.
Markdown is converted to HTML and sanitized.**

Example::

  {% load markdownify %}
  {{'Some *test* [link](#)'|markdownify }}

Is transformed to::

  <p>
    Some <em>test</em> <a href="#">link</a>
  </p>

The source can be found on github_, the docs on `Read the docs`_

.. _django-markup-deprecated: https://pypi.python.org/pypi/django-markup-deprecated
.. _markdown: https://pypi.python.org/pypi/Markdown
.. _bleach: https://pypi.python.org/pypi/bleach
.. _github: https://github.com/RRMoelker/django-markdownify
.. _Read the docs: http://django-markdownify.readthedocs.io/en/latest/