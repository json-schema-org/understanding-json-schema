import json

from docutils import nodes
from docutils import statemachine
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info

import jsonschema


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def split_content(l):
    parts = []
    should_pass = True
    part = []
    language = None

    def add_part():
        if language is None:
            raise ValueError("No language specified")
        parts.append(AttrDict({
            'language': language,
            'content': part}))

    for line in l:
        if line.startswith('--'):
            if len(part):
                add_part()
                part = []
            language = line[2:].strip()
        else:
            part.append(line)

    add_part()

    return parts


class raw_container(nodes.Element):
    pass


def visit_raw_container_node(self, node):
    self.body.append(self.starttag(node, 'div'))


def depart_raw_container_node(self, node):
    self.body.append('</div>')


class tab(nodes.General, nodes.Inline, nodes.Referential, nodes.TextElement):
    pass


def visit_tab_node(self, node):
    atts = {}
    if 'refuri' in node:
        atts['href'] = node['refuri']
        atts['data-toggle'] = 'tab'
    self.body.append(self.starttag(node, 'a', '', **atts))


def depart_tab_node(self, node):
    self.body.append('</a>')


def make_id(self, language):
    return hex(id(self))[2:] + language


class LanguageSpecificDirective(Directive):
    has_content = True

    def run(self):
        parts = split_content(self.content)

        container = raw_container()
        container['classes'] = ['tabbable']

        ul = nodes.bullet_list()
        ul['classes'] = ['nav', 'nav-tabs']
        set_source_info(self, ul)

        href = tab('', 'Language-specific info:')
        paragraph = nodes.paragraph('', '')
        li = nodes.list_item('')
        li['classes'] = ['disabled']

        paragraph.append(href)
        li.append(paragraph)
        ul.append(li)

        first = True
        for part in parts:
            href = tab(part.language, part.language)
            href['refuri'] = '#' + make_id(self, part.language)
            paragraph = nodes.paragraph('')
            li = nodes.list_item('')
            if first:
                li['classes'].append('active')

            paragraph.append(href)
            li.append(paragraph)
            ul.append(li)

            first = False

        container.append(ul)

        pages = raw_container()
        pages['classes'] = ['tab-content']

        first = True
        for part in parts:
            page = raw_container()
            page['classes'] = ['tab-pane']
            if first:
                page['classes'].append('active')
            page['ids'] = [make_id(self, part.language)]

            paragraph = nodes.paragraph('', '')
            content = statemachine.StringList(part.content)
            content.parent = self.content.parent
            self.state.nested_parse(content, 0, paragraph)
            set_source_info(self, paragraph)

            page.append(paragraph)
            pages.append(page)

            first = False

        container.append(pages)

        return [container]


def setup(app):
    app.add_node(tab, html=(visit_tab_node, depart_tab_node))
    app.add_node(raw_container,
                 html=(visit_raw_container_node, depart_raw_container_node))

    app.add_directive('language_specific', LanguageSpecificDirective)
