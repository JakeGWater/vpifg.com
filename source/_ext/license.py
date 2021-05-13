from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives
class license(nodes.General, nodes.Element):
    pass

def visit_license_node(self, node):
    self.body.append(self.starttag(node, 'div', '', CLASS='license'))

def depart_license_node(self, node):
    self.body.append('<div class="license-notice">This content is %s licensed from ' % node['license'])
    self.body.append(f'<a class="license-source", href={node["source_url"]}>{node["source"]}</a>')
    return self.body.append('</div>')

# def yesno(argument):
#     return directives.choice(argument, ('yes', 'no'))

class licenseDirective(SphinxDirective):
    has_content = True
    required_arguments = 1
    option_spec = {
        'source': directives.unchanged,
        'source_url': directives.uri,
    }

    def run(self):
        license_node = license()
        license_node['license'] = self.arguments[0]
        license_node['source'] = self.options['source']
        license_node['source_url'] = self.options['source_url']

        self.state.nested_parse(self.content, self.content_offset, license_node)
        return [license_node]
def setup(app):

    app.add_node(license,
                 html=(visit_license_node, depart_license_node),)
    app.add_directive('license', licenseDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
