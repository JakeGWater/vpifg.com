from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives
class figma(nodes.General, nodes.Element):
    pass

def visit_figma_node(self, node):
    self.body.append(f'<iframe class="figma" style="aspect-ratio: {node["aspect"]}; border: 1px solid rgba(0, 0, 0, 0.1);" width="{node["width"]}" height="{node["height"]}" src="https://www.figma.com/embed?embed_host=share&url={node["refuri"]}"></iframe>')

def depart_figma_node(self, node):
    pass

class figmaDirective(SphinxDirective):
    required_arguments = 1
    option_spec = {
        'width': directives.nonnegative_int,
        'height': directives.nonnegative_int,
        'aspect': directives.unchanged,
    }

    def run(self):
        figma_node = figma()
        figma_node['width'] = self.options.get('width') or "100%"
        figma_node['height'] = self.options.get('height')
        figma_node['refuri'] = self.arguments[0]
        figma_node['aspect'] = self.options.get("aspect") or "16/9"

        return [figma_node]

def setup(app):
    app.add_node(figma,
                 html=(visit_figma_node, depart_figma_node),)
    app.add_directive('figma', figmaDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
