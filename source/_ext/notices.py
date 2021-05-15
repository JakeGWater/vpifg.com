from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives

class notice(nodes.Admonition, nodes.Element):
    pass

def visit_notice_node(self, node):
    self.visit_admonition(node)

def depart_notice_node(self, node):
    self.depart_admonition(node)

class NoticeDirective(SphinxDirective):

    # this enables content in the directive
    has_content = True

    def run(self):
        if self.name == 'wip':
            return self.wip()
        if self.name == 'experimental':
            return self.experimental()
        if self.name == 'planned':
            return self.planned()

    def planned(self):
        notice_node = notice('\n'.join(self.content))
        notice_node += nodes.title(_('Planned'), _('Planned'))
        notice_node['classes'] = ['important']
        textnodes, messages = self.state.paragraph([
            "This content is **Planned**.", 
            "Please see our :doc:`/about/roadmap` for more info."
        ], 0)
        for node in textnodes:
            notice_node += node
        
        self.state.nested_parse(self.content, self.content_offset, notice_node)
        
        return [notice_node]
    
    def wip(self):
        notice_node = notice('\n'.join(self.content))
        notice_node += nodes.title(_('Work In Progress'), _('Work In Progress'))
        notice_node['classes'] = ['warning']
        textnodes, messages = self.state.paragraph([
            "This page is a **Work in Progress** and may be incomplete.",
            "Please see our :doc:`/about/roadmap` for more info."
        ], 0)
        for node in textnodes:
            notice_node += node
        
        self.state.nested_parse(self.content, self.content_offset, notice_node)
        
        return [notice_node]
    
    def experimental(self):
        notice_node = notice('\n'.join(self.content))
        notice_node += nodes.title(_('Work In Progress'), _('Work In Progress'))
        notice_node['classes'] = ['danger']
        textnodes, messages = self.state.paragraph([
            "This page is **Experimental** and may not be Production Ready.",
        ], 0)
        for node in textnodes:
            notice_node += node
        
        self.state.nested_parse(self.content, self.content_offset, notice_node)
        
        return [notice_node]

def setup(app):
    app.add_node(notice,
                 html=(visit_notice_node, depart_notice_node),)                 
    app.add_directive('wip', NoticeDirective)
    app.add_directive('experimental', NoticeDirective)
    app.add_directive('planned', NoticeDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
