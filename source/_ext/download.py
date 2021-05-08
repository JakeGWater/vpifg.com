from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import SphinxDirective
from sphinx.domains import Domain, Index
from sphinx.util.nodes import make_refnode
from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.roles import XRefRole
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives
from sphinx.addnodes import download_reference

class download(download_reference, nodes.Element):
    pass

def visit_download_node(self, node):
    self.body.append(f'<i class="fas fa-download"></i> ')
    self.visit_download_reference(node)

def depart_download_node(self, node):
    self.depart_download_reference(node)

def setup(app):
    app.add_role('download', XRefRole(nodeclass=download), override=True)
    app.add_node(download,
                 html=(visit_download_node, depart_download_node),)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
