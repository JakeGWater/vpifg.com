from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

from notices import notice

class milestone(nodes.General, nodes.Element):
    pass

class roadmap(nodes.General, nodes.Element):
    pass

def visit_roadmap_node(self, node):
    self.body.append("Roadmap")

def depart_roadmap_node(self, node):
    pass

def visit_milestone_node(self, node):
    # self.body.append("Milestone")
    pass

def depart_milestone_node(self, node):
    pass


class RoadmapDirective(SphinxDirective):
    has_content = True
    def run(self):
        name = self.content.pop(0)

        node = roadmap()
        node['name'] = name
        
        self.state.nested_parse(self.content, self.content_offset, node)

        targetid = 'roadmap-%d' % self.env.new_serialno('roadmap')
        targetnode = nodes.target('', '', ids=[targetid])

        if not hasattr(self.env, 'roadmap_all_roadmaps'):
            self.env.roadmap_all_roadmaps = {}

        self.env.roadmap_all_roadmaps[name] = {
            'name': name,
            'docname': self.env.docname,
            'lineno': self.lineno,
            'roadmap': node.deepcopy(),
            'target': targetnode,
        }

        return [targetnode, node]

class MilestoneDirective(SphinxDirective):
    # required_arguments = 1
    has_content = True

    def run(self):
        targetid = 'milestone-%d' % self.env.new_serialno('roadmap')
        targetnode = nodes.target('', '', ids=[targetid])
        name = self.content.pop(0)

        milestone_node = milestone(text=name)
        milestone_node['name'] = name

        if not hasattr(self.env, 'roadmap_all_milestones'):
            self.env.roadmap_all_milestones = []

        self.env.roadmap_all_milestones.append({
            'name': name,
            'docname': self.env.docname,
            'lineno': self.lineno,
            'milestone': milestone_node.deepcopy(),
            'target': targetnode,
        })

        return [targetnode, milestone_node]

def purge_todos(app, env, docname):
    if not hasattr(env, 'roadmap_all_milestones'):
        return

    env.roadmap_all_milestones = [todo for todo in env.roadmap_all_milestones
                          if todo['docname'] != docname]


def merge_todos(app, env, docnames, other):
    if not hasattr(env, 'roadmap_all_milestones'):
        env.roadmap_all_milestones = []
    if hasattr(other, 'roadmap_all_milestones'):
        env.roadmap_all_milestones.extend(other.roadmap_all_milestones)

class planned(nodes.General, nodes.Element):
    pass

def process_todo_nodes(app, doctree, fromdocname):
    # TODO: spit out helpful errors

    env = app.builder.env

    if not hasattr(env, 'roadmap_all_milestones'):
        env.roadmap_all_milestones = []

    if not hasattr(env, 'roadmap_info'):
        env.roadmap_info = {}

    if not hasattr(env, 'roadmap_all_roadmaps'):
        env.roadmap_all_roadmaps = {}

    for node in doctree.traverse(roadmap):
        name = node['name']
        rm = env.roadmap_all_roadmaps[name]
        for z in node.traverse():
            if isinstance(z, planned):
                env.roadmap_info[z['name'].strip()] = rm
                # TODO: optimize this to dictionary
                for ms in env.roadmap_all_milestones:
                    if z['name'] == ms['name']:
                        newnode = nodes.reference('', '')
                        newnode['refdocname'] = ms['docname']
                        newnode['refuri'] = app.builder.get_relative_uri(
                            fromdocname, ms['docname'])
                        newnode['refuri'] += '#' + ms['target']['refid']
                        newnode += nodes.emphasis(text=z['name'])
                        z.replace_self(newnode)

        sec = nodes.section()
        sec += nodes.title(text=f"{name} Roadmap")
        for ch in node:
            sec += ch
        node.replace_self(sec)

    for node in doctree.traverse(milestone):
        name = str(node['name']).strip()
        # TODO: optimize this to dictionary
        if name in env.roadmap_info:
            rm = env.roadmap_info[name]
            notice_node = nodes.admonition()
            notice_node += nodes.title(_('Planned'), _('Planned'))
            notice_node['classes'] = ['important']
            p = nodes.paragraph(text=f"""This item is planned in the """)

            newnode = nodes.reference('', '')
            newnode['refdocname'] = rm['docname']
            newnode['refuri'] = app.builder.get_relative_uri(
                fromdocname, rm['docname'])
            newnode['refuri'] += '#' + rm['target']['refid']
            newnode += nodes.emphasis(text=f"""{rm['name']} Roadmap.""")

            p += newnode
            notice_node += p

            node.replace_self(notice_node)
    
    for node in doctree.traverse(milestone):
        notice_node = nodes.admonition()
        notice_node += nodes.title(_('Help Wanted'), _('Help Wanted'))

        newnode = nodes.reference('', '')
        newnode['refdocname'] = 'about/roadmap'
        newnode['refuri'] = app.builder.get_relative_uri(fromdocname, 'about/roadmap')
        newnode += nodes.emphasis(text=f"""Roadmaps""")

        p = nodes.paragraph()
        p += nodes.inline(text=f"""This page is not currently planned. As such, there is no estimate on when it might get completed. See """)
        p += newnode
        p += nodes.inline(text=" for more info.")

        notice_node += p

        p = nodes.paragraph(text="Check out our ")

        newnode = nodes.reference('', '')
        newnode['refdocname'] = 'about/contributing'
        newnode['refuri'] = app.builder.get_relative_uri(fromdocname, 'about/contributing')
        newnode += nodes.emphasis(text=f"""Contributing Guide""")

        p += newnode
        p += nodes.inline(text=" if you would like to help maintain this content.")

        notice_node += p

        node.replace_self(notice_node)

def visit_planned_node(self, node):
    self.body.append("planned")

def depart_planned_node(self, node):
    pass

def planned_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = planned()
    node['name'] = text
    return [node], []

def setup(app):
    # app.add_config_value('todo_include_todos', False, 'html')

    app.add_node(roadmap,
                html=(visit_roadmap_node, depart_roadmap_node))
    app.add_node(milestone,
                 html=(visit_milestone_node, depart_milestone_node))

    app.connect('doctree-resolved', process_todo_nodes)

    app.add_directive('roadmap', RoadmapDirective)
    app.add_directive('milestone', MilestoneDirective)
    app.add_role('planned', planned_role)

    app.connect('env-purge-doc', purge_todos)
    app.connect('env-merge-info', merge_todos)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
