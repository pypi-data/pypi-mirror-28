#! -*- coding: utf-8 -*-
"""
    modelsdoc.templatetags.modelsdoc_tags
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k  <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import, unicode_literals  # NOQA

from django.template import Library, Node

register = Library()


class EmptylinelessNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        lines = []
        for line in self.nodelist.render(context).strip().split('\n'):
            if not line.strip():
                continue
            lines.append(line)
        return '\n'.join(lines)


@register.tag
def emptylineless(parser, token):
    """
    Removes empty line.

    Example usage::

        {% emptylineless %}
            test1

            test2

            test3
        {% endemptylineless %}

    This example would return this HTML::

            test1
            test2
            test3

    """
    nodelist = parser.parse(('endemptylineless',))
    parser.delete_first_token()
    return EmptylinelessNode(nodelist)


@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr, '')


@register.filter
def str_repeat(times, string):
    return string * times
