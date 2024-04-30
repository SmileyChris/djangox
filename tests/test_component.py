import re

import pytest
from django.template import Context, TemplateSyntaxError
from django.template.loader import render_to_string
from django.test import override_settings

from includecontents.base import Template


def test_basic():
    assert render_to_string("test_component/index.html") == (
        """<main>
  <section class="card">
  <h3 >hello</h3>
  <div>some content</div>
</section>
</main>
"""
    )


@override_settings(DEBUG=True)
def test_debug_mode():
    render_to_string("test_component/index.html")


def test_attrs():
    assert render_to_string("test_component/attrs.html") == (
        """<main>
  <section class="mycard" id="topcard">
  <h3 class="large">hello</h3>
  <div>
    some content
  </div>
</section>
</main>
"""
    )


def test_missing_attr():
    with pytest.raises(
        TemplateSyntaxError,
        match='Missing required attribute "title" in <include:card>',
    ):
        render_to_string("test_component/missing_attr.html")


def test_missing_closing_tag():
    with pytest.raises(
        TemplateSyntaxError,
        match=re.compile(r"Unclosed tag.*<include:card>.*</include:card>"),
    ):
        render_to_string("test_component/missing_closing_tag.html")


def test_extend_class():
    assert render_to_string("test_component/extend_class.html") == (
        """<main>
  <section class="mycard card lg">
  <h3 >hello</h3>
  <div>
    some content
  </div>
</section>
</main>
"""
    )

    assert render_to_string("test_component/extend_class.html", {"red": True}) == (
        """<main>
  <section class="mycard card lg">
  <h3 class="text-red">hello</h3>
  <div>
    some content
  </div>
</section>
</main>
"""
    )


def test_empty_props():
    output = Template(
        "Attrs: <include:empty-props id='1' hello></include:empty-props>"
    ).render(Context())
    assert output == 'Attrs: id="1" hello/'


def test_only_advanced_props():
    output = Template(
        "Attrs: <include:empty-props inner.id='1'></include:empty-props>"
    ).render(Context())
    assert output == 'Attrs: /id="1"'


def test_nested_attrs():
    output = Template(
        "<include:nested-attrs inner.class='2' class='1'></include:nested-attrs>"
    ).render(Context())
    assert (
        output
        == """\
<div class="1 main"></div>
<div class="2 inner"></div>"""
    )
