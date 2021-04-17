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
        textnodes, messages = self.state.paragraph(["This page is a **Work in Progress** and may be incomplete."], 0)
        for node in textnodes:
            notice_node += node
        
        self.state.nested_parse(self.content, self.content_offset, notice_node)
        
        return [notice_node]
    
    def experimental(self):
        notice_node = notice('\n'.join(self.content))
        notice_node += nodes.title(_('Work In Progress'), _('Work In Progress'))
        notice_node['classes'] = ['danger']
        textnodes, messages = self.state.paragraph([
            "This page is **Experimental** and may not be :term:`Production Ready`.",
        ], 0)
        for node in textnodes:
            notice_node += node
        
        self.state.nested_parse(self.content, self.content_offset, notice_node)
        
        return [notice_node]


class prodcheck(nodes.Admonition, nodes.Element):
    pass

def visit_prodcheck_node(self, node):
    self.visit_admonition(node)

def depart_prodcheck_node(self, node):
    self.depart_admonition(node)

def yesno(argument):
    return directives.choice(argument, ('yes', 'no'))

ProdCheckS = {
    '4k': '4K',
    'raw': 'RAW',
    'timecode': 'Timecode',
    'aces': 'ACES',
    'live': 'Live',
    'multicam': 'Multicam',
    'ndisplay': 'nDisplay'
}

class prodcheckDirective(SphinxDirective):
    option_spec = {
        '4k': yesno,
        'raw': yesno,
        'timecode': yesno,
        'aces': yesno,
        'live': yesno,
        'multicam': yesno,
        'ndisplay': yesno
    }

    def run(self):
        ncols = len(self.option_spec.keys())
        table = nodes.table()
        tgroup = nodes.tgroup(cols=ncols)
        header = nodes.row()
        checks = nodes.row()
        for key in self.option_spec.keys():
            field = nodes.entry()
            par = nodes.paragraph()
            ref, _ = self.state.inline_text(text=":term:`%s`" % ProdCheckS[key], lineno=0)
            par += ref
            field += par
            header += field
            if self.options[key] == 'yes':
                check = '✅'
            else:
                check = '❌'
            field = nodes.entry()
            field += nodes.paragraph(text=check)
            checks += (field)
        head = nodes.thead()
        body = nodes.tbody()
        head += header
        body += checks
        for _ in range(ncols):
            colspec = nodes.colspec(colwidth=1)
            tgroup += colspec
        tgroup += head
        tgroup += body
        table += tgroup
        table['class'] = ['prodcheck']
        adm = nodes.admonition()
        title = nodes.title(text="Production Checklist")
        adm += title
        adm += table
        cont = nodes.container()
        cont['classes'] = ['prodcheck']
        cont['class'] = ['prodcheck']
        cont += adm
        return [cont]

def setup(app):
    # app.add_config_value('todo_include_todos', False, 'html')
    app.add_node(notice,
                 html=(visit_notice_node, depart_notice_node),)                 
    app.add_directive('wip', NoticeDirective)
    app.add_directive('experimental', NoticeDirective)
    app.add_directive('planned', NoticeDirective)

    app.add_node(prodcheck,
                 html=(visit_prodcheck_node, depart_prodcheck_node),)
    app.add_directive('prodcheck', prodcheckDirective)

    # app.add_directive('todolist', TodolistDirective)
    # app.connect('doctree-resolved', process_notice_nodes)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
