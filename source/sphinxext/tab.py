from docutils import nodes
from docutils import statemachine
from docutils.parsers.rst import Directive
import re


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def split_content(l):
    parts = []
    part = []
    label = None

    def add_part():
        if label is None:
            raise ValueError("No label specified")
        parts.append(AttrDict({
            'label': label,
            'content': part}))

    for line in l:
        if line.startswith('--'):
            if len(part):
                add_part()
                part = []
            label = line[2:].strip()
        else:
            part.append(line)

    add_part()

    return parts


class pages(nodes.Element):
    local_attributes = ['parts']

    def __init__(self, *args, **kwargs):
        self.parts = kwargs['parts']
        nodes.Element.__init__(self, *args, **kwargs)


class language_specific_pages(pages):
    header = 'Language-specific info:'


class draft_pages(pages):
    header = 'Draft-specific info:'


class section(nodes.Element):
    pass


def visit_pages_node_html(self, node):
    node['classes'] = ['tabbable']

    ul = nodes.bullet_list()
    ul['classes'] = ['nav', 'nav-tabs']
    # set_source_info(self, ul)

    href = tab('', node.header)
    href['classes'] = ['disabled']
    paragraph = nodes.paragraph('', '')
    li = nodes.list_item('')
    li['classes'] = ['disabled']

    paragraph.append(href)
    li.append(paragraph)
    ul.append(li)

    first = True
    for part in node.parts:
        href = tab(part.label, part.label)
        href['refuri'] = '#' + make_id(node, part.label)
        paragraph = nodes.paragraph('')
        li = nodes.list_item('')
        if first:
            li['classes'].append('active')

        paragraph.append(href)
        li.append(paragraph)
        ul.append(li)

        first = False

    node.append(ul)

    pages = section()
    pages['classes'] = ['tab-content']

    first = True
    for part in node.parts:
        page = section()
        page['classes'] = ['tab-pane']
        if first:
            page['classes'].append('active')
        page['ids'] = [make_id(node, part.label)]

        page.append(part.paragraph)
        pages.append(page)

        first = False

    node.append(pages)

    self.body.append(self.starttag(node, 'div'))


def depart_pages_node_html(self, node):
    self.body.append('</div>')


def visit_pages_node_latex(self, node):
    for part in node.parts:
        t = tab('', '')
        t.label = part.label
        t.append(part.paragraph)
        node.append(t)


def depart_pages_node_latex(self, node):
    pass


class tab(nodes.General, nodes.Inline, nodes.Referential, nodes.TextElement):
    pass


def visit_tab_node_html(self, node):
    atts = {}
    if 'refuri' in node:
        atts['href'] = node['refuri']
        atts['data-toggle'] = 'tab'
    self.body.append(self.starttag(node, 'a', '', **atts))


def depart_tab_node_html(self, node):
    self.body.append('</a>')


def visit_tab_node_latex(self, node):
    self.body.append(r'\begin{jsonframe}{%s}{black}' % node.label)


def depart_tab_node_latex(self, node):
    self.body.append(r'\end{jsonframe}')


def make_id(self, label):
    return '{0}_{1}'.format(hex(id(self))[2:], re.sub(r"\W", "_", label))


class TabDirective(Directive):
    has_content = True

    def run(self):
        parts = split_content(self.content)
        container = self.make_container(parts)

        for part in parts:
            paragraph = nodes.paragraph('', '')
            content = statemachine.StringList(part.content)
            content.parent = self.content.parent
            self.state.nested_parse(content, 0, paragraph)
            part.paragraph = paragraph

        return [container]


class LanguageSpecificDirective(TabDirective):
    def make_container(self, parts):
        return language_specific_pages(parts=parts)


class DraftDirective(TabDirective):
    def make_container(self, parts):
        return draft_pages(parts=parts)


def setup(app):
    app.add_node(tab,
                 html=(visit_tab_node_html, depart_tab_node_html),
                 latex=(visit_tab_node_latex, depart_tab_node_latex))
    app.add_node(language_specific_pages,
                 html=(visit_pages_node_html,
                       depart_pages_node_html),
                 latex=(visit_pages_node_latex,
                        depart_pages_node_latex))
    app.add_node(draft_pages,
                 html=(visit_pages_node_html,
                       depart_pages_node_html),
                 latex=(visit_pages_node_latex,
                        depart_pages_node_latex))

    app.add_directive('language_specific', LanguageSpecificDirective)
    app.add_directive('draft_specific', DraftDirective)


latex_preamble = r"""
  \usepackage{mdframed}
  \usepackage{tikz}

  \newenvironment{jsonframe}[2]{%
  \ifstrempty{#1}%
  {}%
  {\mdfsetup{%
    skipabove=10pt,
    frametitle={%
    \tikz[baseline=(current bounding box.east),outer sep=0pt,text=white]
    \node[anchor=east,rectangle,fill=#2]
    {\strut \textsf{ #1 }};}}%
   }%
   \mdfsetup{innertopmargin=10pt,linecolor=#2,%
             skipabove=10pt,
             linewidth=1pt,topline=true,nobreak=true,
             frametitleaboveskip=\dimexpr-\ht\strutbox\relax,}
   \begin{mdframed}[]\relax%
   }{\end{mdframed}}
"""
