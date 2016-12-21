import json

from docutils import nodes
from docutils import statemachine
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info
from sphinx.util import parselinenos

import jsonschema


class jsonschema_node(nodes.Element):
    pass


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def split_content(l):
    parts = []
    should_pass = True
    part = []
    comment = []

    def add_part():
        hl_lines = []
        for i, line in enumerate(part):
            if line.lstrip().startswith('*'):
                line = line.replace('*', '', 1)
                hl_lines.append(i + 1)
                part[i] = line

        content = '\n'.join(part)
        try:
            json_content = json.loads(content)
        except ValueError:
            if should_pass:
                raise ValueError("Invalid json: {0}".format(content))
            else:
                # A complex number will never validate
                json_content = 1+1j
        parts.append(AttrDict({
            'should_pass': should_pass,
            'content': content,
            'json': json_content,
            'comment': comment,
            'hl_lines': hl_lines}
        ))

    for line in l:
        if line.startswith('//'):
            comment.append(line[2:].lstrip())
        elif line == '--':
            add_part()
            should_pass = True
            part = []
            comment = []
        elif line == '--X':
            add_part()
            should_pass = False
            part = []
            comment = []
        else:
            part.append(line)

    add_part()

    return parts[0], parts[1:]


class SchemaExampleDirective(Directive):
    has_content = True
    validate = True


    def run(self):
        result = []

        schema, parts = split_content(self.content)

        container = jsonschema_node()
        set_source_info(self, container)

        literal = nodes.literal_block(
            schema.content, schema.content)
        literal['language'] = 'javascript'
        literal['classes'] = container['classes'] = ['jsonschema']
        if schema.hl_lines:
            literal['highlight_args'] = {'hl_lines': schema.hl_lines}
        set_source_info(self, literal)
        container.append(literal)
        result.append(container)

        for part in parts:
            if self.validate:
                is_valid = True
                try:
                    jsonschema.validate(part.json, schema.json)
                except jsonschema.ValidationError as e:
                    is_valid = False
                except jsonschema.SchemaError as e:
                    raise ValueError("Schema is invalid:\n{0}\n\n{1}".format(
                        str(e), schema.content))

                if is_valid != part.should_pass:
                    if part.should_pass:
                        raise ValueError(
                            "Doc says fragment should pass, "
                            "but it does not validate:\n" +
                            part.content)
                    else:
                        raise ValueError(
                            "Doc says fragment should not pass, "
                            "but it validates:\n" +
                            part.content)
            else:
                is_valid = part.should_pass

            if len(part.comment):
                paragraph = nodes.paragraph('', '')
                comment = statemachine.StringList(part.comment)
                comment.parent = self.content.parent
                self.state.nested_parse(comment, 0, paragraph)
                paragraph['classes'] = ['jsonschema-comment']
                set_source_info(self, paragraph)
                result.append(paragraph)

            container = jsonschema_node()
            set_source_info(self, container)
            literal = nodes.literal_block(
                part.content, part.content)
            literal['language'] = 'javascript'
            if is_valid:
                literal['classes'] = container['classes'] = ['jsonschema-pass']
            else:
                literal['classes'] = container['classes'] = ['jsonschema-fail']
            if part.hl_lines:
                literal['highlight_args'] = {'hl_lines': part.hl_lines}
            set_source_info(self, literal)
            container.append(literal)
            result.append(container)

        return result


class SchemaExampleNoValidationDirective(SchemaExampleDirective):
    validate = False


def visit_jsonschema_node_html(self, node):
    pass


def depart_jsonschema_node_html(self, node):
    pass


def visit_jsonschema_node_latex(self, node):
    adjust = False
    color = "gray"
    char = ""
    if 'jsonschema-pass' in node['classes']:
        char = r"\Checkmark"
        color = "ForestGreen"
        adjust = True
    elif 'jsonschema-fail' in node['classes']:
        char = r"\XSolidBrush"
        color = "BrickRed"
        adjust = True
    elif 'jsonschema' in node['classes']:
        char = r"\{ json schema \}"

    if adjust:
        self.body.append(r"\begin{adjustwidth}{2.5em}{0pt}")
    self.body.append(r"\begin{jsonframe}{%s}{%s}" % (char, color))


def depart_jsonschema_node_latex(self, node):
    adjust = False
    if 'jsonschema-pass' in node['classes']:
        adjust = True
    elif 'jsonschema-fail' in node['classes']:
        adjust = True

    self.body.append(r"\end{jsonframe}")
    if adjust:
        self.body.append(r"\end{adjustwidth}")


def setup(app):
    app.add_directive('schema_example', SchemaExampleDirective)
    app.add_directive('schema_example_novalid',
                      SchemaExampleNoValidationDirective)

    app.add_node(jsonschema_node,
                 html=(visit_jsonschema_node_html, depart_jsonschema_node_html),
                 latex=(visit_jsonschema_node_latex, depart_jsonschema_node_latex))

passoptionstopackages = r'\PassOptionsToPackage{dvipsnames}{xcolor}'

latex_preamble = r"""
\usepackage{changepage}
\usepackage{xcolor}
"""
