from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives

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
    app.add_node(prodcheck,
                 html=(visit_prodcheck_node, depart_prodcheck_node),)
    app.add_directive('prodcheck', prodcheckDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
