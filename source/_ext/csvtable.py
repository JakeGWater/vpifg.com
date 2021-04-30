from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives

class csv(nodes.General, nodes.Element):
    pass

def visit_csv_node(self, node):
    self.body.append(f'<iframe class="csv" style="aspect-ratio: {node["aspect"]}; border: 1px solid rgba(0, 0, 0, 0.1);" width="{node["width"]}" height="{node["height"]}" src="/csv#table={node["refuri"]}"></iframe>')

def depart_csv_node(self, node):
    pass

class csvDirective(SphinxDirective):
    required_arguments = 1
    option_spec = {
        'width': directives.nonnegative_int,
        'height': directives.nonnegative_int,
        'aspect': directives.unchanged,
    }

    def run(self):
        csv_node = csv()
        csv_node['width'] = self.options.get('width') or "100%"
        csv_node['height'] = self.options.get('height')
        csv_node['refuri'] = self.arguments[0]
        csv_node['aspect'] = self.options.get("aspect") or "16/9"

        return [csv_node]

def setup(app):
    app.add_node(csv,
                 html=(visit_csv_node, depart_csv_node),)
    app.add_directive('csv', csvDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
