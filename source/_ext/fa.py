from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import SphinxDirective
from sphinx.domains import Domain, Index
from sphinx.util.nodes import make_refnode
from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives

class fa(nodes.General, nodes.Element):
    pass

def visit_fa_node(self, node):
    icon = node['icon']
    self.body.append(f'<i class="fas fa-{icon}"></i>')

def depart_fa_node(self, node):
    pass

def fa_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    icon = fa()
    icon['icon'] = text
    return [[icon], []]

def setup(app):
    app.add_role('fa', fa_role)
    app.add_node(fa,
                 html=(visit_fa_node, depart_fa_node),)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
