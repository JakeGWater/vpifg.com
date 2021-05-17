from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, SphinxRole

from notices import notice

class milestone(nodes.General, nodes.Element):
    pass

class roadmap(nodes.General, nodes.Element):
    pass

class backlog(nodes.General, nodes.Element):
    pass

class BacklogDirective(SphinxDirective):
    def run(self):
        return [backlog()]

class RoadmapDirective(SphinxDirective):
    has_content = True
    def run(self):
        name = self.content[0]

        node = roadmap()
        node['name'] = name

        self.state.nested_parse(self.content[1:], self.content_offset, node)

        if not hasattr(self.env, 'roadmap_all_roadmaps'):
            self.env.roadmap_all_roadmaps = {}

        if not hasattr(self.env, 'roadmap_all_planned'):
            self.env.roadmap_all_planned = {}

        for n in node.traverse(condition=planned):
            self.env.roadmap_all_planned[n['name']] = name

        node = roadmap()
        node['name'] = name        
        self.state.nested_parse(self.content[1:], self.content_offset, node)

        targetid = 'roadmap-%d' % self.env.new_serialno('roadmap')
        targetnode = nodes.target('', '', ids=[targetid])

        self.env.roadmap_all_roadmaps[name] = {
            'name': name,
            'docname': self.env.docname,
            'lineno': self.lineno,
            'roadmap': node.deepcopy(),
            'target': targetnode,
        }

        return [targetnode, node]

class PlannedRole(SphinxRole):
    def run(self):
        node = planned()
        node['name'] = self.text
        return [node], []

class findroadmap(nodes.General, nodes.Element):
    pass

class FindRoadmapRole(SphinxRole):
    def run(self):
        return [findroadmap()], []

class goto(nodes.General, nodes.Element):
    pass

class GotoRole(SphinxRole):
    def run(self):
        node = goto()
        node['doc'] = self.text
        return [node], []

class MilestoneDirective(SphinxDirective):
    def run(self):
        targetid = 'milestone-%d' % self.env.new_serialno('roadmap')
        targetnode = nodes.target('', '', ids=[targetid])

        name = self.env.docname

        milestone_node = milestone(text=name)
        milestone_node['name'] = name

        if 'roadmap' in self.env.app.config:
            conf = self.env.app.config['roadmap']
        else:
            conf = CONFIG_DEFAULTS

        message_vars = {
            'roadmap': name
        }

        backlog_container = nodes.container()
        for line in conf['backlog_message']:
            backlog_message, _messages = self.state.inline_text(line.format(**message_vars), 0)
            p = nodes.paragraph()
            p += backlog_message
            backlog_container += p

        roadmap_container = nodes.container()
        for line in conf['roadmap_message']:
            roadmap_message, _messages = self.state.inline_text(line.format(**message_vars), 0)
            p = nodes.paragraph()
            p += roadmap_message
            roadmap_container += p

        milestone_node += backlog_container
        milestone_node += roadmap_container

        if not hasattr(self.env, 'roadmap_all_milestones'):
            self.env.roadmap_all_milestones = {}

        self.env.roadmap_all_milestones[name] = {
            'name': name,
            'docname': self.env.docname,
            'lineno': self.lineno,
            'milestone': milestone_node.deepcopy(),
            'target': targetnode,
        }

        return [targetnode, milestone_node]

def purge_todos(app, env, docname):
    if not hasattr(env, 'roadmap_all_milestones'):
        return

    # env.roadmap_all_milestones = [todo for todo in env.roadmap_all_milestones
    #                       if todo['docname'] != docname]

def merge_todos(app, env, docnames, other):
    if not hasattr(env, 'roadmap_all_milestones'):
        env.roadmap_all_milestones = {}
    if hasattr(other, 'roadmap_all_milestones'):
        env.roadmap_all_milestones.extend(other.roadmap_all_milestones)

class planned(nodes.General, nodes.Element):
    pass

def process_todo_nodes(app, doctree, fromdocname):
    # TODO: spit out helpful errors

    env = app.builder.env
    
    # Search roadmaps and catalogue all of the <planned> roles
    for node in doctree.traverse(roadmap):
        name = node['name']
        for z in node.traverse(condition=planned):
            # TODO: optimize this to dictionary
            zname = z['name']
            if zname in env.roadmap_all_milestones:
                ms = env.roadmap_all_milestones[zname]
                newnode = nodes.reference('', '')
                newnode['refdocname'] = ms['docname']
                newnode['refuri'] = app.builder.get_relative_uri(fromdocname, ms['docname'])
                newnode['refuri'] += '#' + ms['target']['refid']
                title = env.titles[ms['docname']]
                newnode += nodes.inline(text=title.astext())
                z.replace_self(newnode)
            else:
                raise RuntimeError("OOPS")
        sec = nodes.section()
        sec += nodes.title(text=f"{name} Roadmap")
        for ch in node:
            sec += ch
        node.replace_self(sec)

    for node in doctree.traverse(planned):
        node.replace_self(nodes.emphasis(text=f"{node['name']} (Unknown Milestone)"))

    for node in doctree.traverse(milestone):
        name = node['name']
        if name in env.roadmap_all_planned:
            rm = env.roadmap_all_roadmaps[env.roadmap_all_planned[name]]
            notice_node = nodes.admonition()
            notice_node += nodes.title(text=('Sorry! This page has not been created yet'))
            notice_node['classes'] = ['attention']
            
            p = node[1]

            for fr in node.traverse(condition=findroadmap):
                newnode = nodes.reference('', '')
                newnode['refdocname'] = rm['docname']
                newnode['refuri'] = app.builder.get_relative_uri(fromdocname, rm['docname'])
                newnode['refuri'] += '#' + rm['target']['refid']
                newnode += nodes.inline(text=f"""{rm['name']} Roadmap""")
                fr.replace_self(newnode)

            notice_node += p

            node.replace_self(notice_node)
    
    for node in doctree.traverse(milestone):
        notice_node = nodes.admonition()
        notice_node += nodes.title(_('Help Wanted'), _('Help Wanted'))
        notice_node += nodes.title(text='Sorry! This page has not been created yet')
        notice_node['classes'] = ['danger']

        newnode = nodes.reference('', '')
        newnode['refdocname'] = 'about/roadmap'
        newnode['refuri'] = app.builder.get_relative_uri(fromdocname, 'about/roadmap')
        newnode += nodes.inline(text=f"""Roadmaps""")

        p = node[0]
        notice_node += p

        node.replace_self(notice_node)

    for node in doctree.traverse(backlog):
        ul = nodes.bullet_list()
        for docname in env.roadmap_all_milestones:
            li = nodes.list_item()
            if docname not in env.roadmap_all_planned:
                ref = nodes.reference('', '')
                ref['refdocname'] = docname
                ref['refuri'] = app.builder.get_relative_uri(fromdocname, docname)
                title = env.titles[docname].astext()
                ref += nodes.inline(text=title)
                p = nodes.paragraph()
                p += ref
                li += p
                ul += li
        node.replace_self(ul)
    
    for node in doctree.traverse(goto):
        docname = node['doc']
        il = nodes.inline()
        ref = nodes.reference('', '')
        ref['refdocname'] = docname
        ref['refuri'] = app.builder.get_relative_uri(fromdocname, docname)

        if docname in env.titles:
            title = env.titles[docname].astext()
        else:
            title = docname
        ref += nodes.inline(text=title)
        il += ref
        
        if docname in env.roadmap_all_milestones:
            if docname in env.roadmap_all_planned:
                text = "Planned"
                gl = nodes.inline(text=text, classes=['planned'])
                ref['classes'] = ['roadmap']
            else:
                text = "Help Wanted"
                gl = nodes.inline(text=text, classes=['helpwanted'])
                ref['classes'] = ['backlog']
            il += gl

        node.replace_self(il)

def visit_planned_node(self, node):
    self.body.append("planned")

def depart_planned_node(self, node):
    pass

CONFIG_DEFAULTS = {
    'backlog_message': ["Backlog"],
    'roadmap_message': ["Roadmap"],
}

def setup(app):
    # app.add_config_value('todo_include_todos', False, 'html')

    # app.add_node(roadmap,
    #             html=(visit_roadmap_node, depart_roadmap_node))
    # app.add_node(milestone,
    #              html=(visit_milestone_node, depart_milestone_node))

    app.add_config_value('roadmap', CONFIG_DEFAULTS, 'html')

    app.connect('doctree-resolved', process_todo_nodes)

    app.add_directive('roadmap', RoadmapDirective)
    app.add_directive('backlog', BacklogDirective)
    app.add_directive('milestone', MilestoneDirective)
    app.add_role('planned', PlannedRole())
    app.add_role('findroadmap', FindRoadmapRole())
    app.add_role('goto', GotoRole())

    # app.connect('env-purge-doc', purge_todos)
    # app.connect('env-merge-info', merge_todos)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
