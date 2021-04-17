from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

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

class Avatar(nodes.General, nodes.Element):
    pass

def visit_Avatar_node(self, node):
    self.body.append(self.starttag(node, 'div', '', CLASS='avatar'))

def depart_Avatar_node(self, node):
    self.body.append('</div>')

class AvatarDirective(SphinxDirective):
    option_spec = {
        # 'class': directives.unchanged,
        # 'revisions': directives.nonnegative_int,
        # 'rev-list': six.text_type,
        # 'detailed-message-pre': bool,
        # 'detailed-message-strong': bool,
        # 'filename_filter': six.text_type,
        # 'hide_author': bool,
        # 'hide_date': bool,
        # 'hide_details': bool,
        # 'repo-dir': six.text_type,
    }

    has_content = True
    required_arguments=1

    def run(self):
        avatar = Avatar()
        imgurl = self.arguments[0]

        imgbox = nodes.container()
        imgbox['classes'] = ['avatar-image']
        
        image = nodes.image()
        image['uri'] = imgurl
        
        imgbox += image
        
        text = nodes.container()
        text['classes'] = ['avatar-introduction']

        self.state.nested_parse(self.content, self.content_offset, text)

        avatar += text
        avatar += imgbox

        # clear = nodes.container()
        # clear['classes'] = ['avatar-clear']
        # avatar += clear

        return [avatar]

class Clear(nodes.General, nodes.Element):
    pass

def visit_Clear_node(self, node):
    self.body.append(self.starttag(node, 'div', '', CLASS='clear'))

def depart_Clear_node(self, node):
    self.body.append('</div>')

class ClearDirective(SphinxDirective):
    def run(self):
        return [Clear()]

def setup(app):
    app.add_node(Avatar,
                html=(visit_Avatar_node, depart_Avatar_node),)
    app.add_directive('avatar', AvatarDirective)

    app.add_directive('clear', ClearDirective)
    app.add_node(Clear,
                 html=(visit_Clear_node, depart_Clear_node),)


    # app.add_config_value('todo_include_todos', False, 'html')
    app.add_node(notice,
                 html=(visit_notice_node, depart_notice_node),)
                 
    app.add_directive('wip', NoticeDirective)
    app.add_directive('experimental', NoticeDirective)
    app.add_directive('planned', NoticeDirective)

    # app.add_directive('todolist', TodolistDirective)
    # app.connect('doctree-resolved', process_notice_nodes)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
