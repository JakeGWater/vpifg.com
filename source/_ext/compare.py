from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives

class imgCompare(nodes.Admonition, nodes.Element):
    pass

def visit_imgCompare_node(self, node):
    self.body.append(f'<div class="compare-image">')
    self.body.append((f"""
<split-view>
  <picture slot="top">
    <img src="{node['left']}" alt="" />
  </picture>
  <picture slot="bottom">
    <img src="{node['right']}" alt="" />
  </picture>
</split-view>
    """))

def depart_imgCompare_node(self, node):
    self.body.append('</div>')

class imgCompareDirective(SphinxDirective):
    has_content = True

    option_spec = {
        'left': directives.uri,
        'right': directives.uri,
        'width': directives.nonnegative_int,
        'height': directives.nonnegative_int,
    }

    def run(self):
        img = imgCompare()
        img['left'] = self.options.get('left')
        img['right'] = self.options.get('right')
        img['width'] = self.options.get('width')
        img['height'] = self.options.get('height')

        self.state.nested_parse(self.content, self.content_offset, img)

        return [img]

def setup(app):
    app.add_node(imgCompare,
                 html=(visit_imgCompare_node, depart_imgCompare_node),)                 
    app.add_directive('compare', imgCompareDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
