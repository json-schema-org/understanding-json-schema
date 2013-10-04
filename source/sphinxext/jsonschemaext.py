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
    comment = []

    def add_part():
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
            'comment': comment}))

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

        literal = nodes.literal_block(
            schema.content, schema.content)
        literal['language'] = 'javascript'
        literal['classes'] = ['jsonschema']
        set_source_info(self, literal)
        result.append(literal)

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

            literal = nodes.literal_block(
                part.content, part.content)
            literal['language'] = 'javascript'
            if is_valid:
                literal['classes'] = ['jsonschema-pass']
            else:
                literal['classes'] = ['jsonschema-fail']
            set_source_info(self, literal)
            result.append(literal)

        return result


class SchemaExampleNoValidationDirective(SchemaExampleDirective):
    validate = False


def setup(app):
    app.add_directive('schema_example', SchemaExampleDirective)
    app.add_directive('schema_example_novalid',
                      SchemaExampleNoValidationDirective)
