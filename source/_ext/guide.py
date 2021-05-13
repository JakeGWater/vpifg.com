from collections import defaultdict

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription, SphinxDirective
from sphinx.domains import Domain, Index
from sphinx.roles import XRefRole, SphinxRole
from sphinx.util.nodes import make_refnode
from sphinx.errors import SphinxError

def DEBUG(msg):
    # print(f"---{msg}---")
    pass

class showdeps(nodes.General, nodes.Element):
    pass

class ShowDepsDirective(SphinxDirective):
    def run(self):
        DEBUG("DepsDirective")
        return [showdeps()]

def visit_deps(self, node):
    self.body.append(f"""
        <div class="topic guide-showdeps">
        <p class="topic-title">Pre-Requisites</p>
        """
    )

def depart_deps(self, node):
    self.body.append(f"""
        </div>
        """
    )

class shownexts(nodes.General, nodes.Element):
    pass

def visit_shownexts(self, node):
    self.body.append(f"""
        <div class="topic guide-shownexts">
        <p class="topic-title">Next Steps</p>
        """
    )

def depart_shownexts(self, node):
    self.body.append(f"""
        </div>
        """
    )

class ShowNextsDirective(SphinxDirective):
    def run(self):
        DEBUG("NextsDirective")
        return [shownexts()]

class lesson(nodes.General, nodes.Element):
    pass

class LessonDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    # option_spec = {
    #     # 'contains': directives.unchanged_required,
    # }
    def run(self):
        DEBUG("LESSONDIRECTIVE")
        node = lesson()
        self.state.nested_parse(self.content, self.content_offset - 1, node)
        return [node]
    
def visit_lesson(self, node):
    self.body.append(f"""
        <div class="topic guide-lesson">
        <p class="topic-title">Lesson Plan</p>
        """
    )

def depart_lesson(self, node):
    self.body.append(f"""
        </div>
        """
    )
        
class dep(nodes.General, nodes.Element):
    pass

class DepDirective(SphinxDirective):
    has_content = True
    def run(self):
        node_dep = dep()
        title = self.content.pop(0)
        targetid = 'guide-%d' % self.env.new_serialno('guide')
        node_dep['title'] = title
        node_dep['targetid'] = targetid
        DEBUG(targetid)
        self.state.nested_parse(self.content, self.content_offset - 1, node_dep)
        return [node_dep]

def visit_dep(self, node):
    targetid = node['targetid']
    title = node['title']
    self.body.append(f"""
        <div class="guide-dep admonition" id="{targetid}">
        <p class="admonition-title">{title}</p>
        <div class="docutils container">
        """
    )

def depart_dep(self, node):
    self.body.append(f"""
        </div>
        </div>
        """
    )

class next(nodes.General, nodes.Element):
    pass

class NextDirective(SphinxDirective):
    has_content=True
    def run(self):
        node_dep = next()
        title = self.content.pop(0)
        targetid = 'guide-%d' % self.env.new_serialno('guide')
        node_dep['title'] = title
        node_dep['targetid'] = targetid
        DEBUG(targetid)
        self.state.nested_parse(self.content, self.content_offset - 1, node_dep)
        return [node_dep]

def visit_next(self, node):
    targetid = node['targetid']
    title = node['title']
    self.body.append(f"""
        <div class="guide-next admonition" id="{targetid}">
        <p class="admonition-title">{title}</p>
        <div class="docutils container">
        """
    )

def depart_next(self, node):
    self.body.append(f"""
        </div>
        </div>
        """
    )

class help(nodes.General, nodes.Element):
    pass

class HelpRole(SphinxRole):
    def run(self):
        return [next()], []

class GuideDomain(Domain):
    name = 'guide'
    label = 'Guide Inter-linking'
    roles = {
        # 'dep': DepRole(),
        # 'next': NextRole(),
        # 'help': HelpRole(),
    }
    directives = {
        'lesson': LessonDirective,
        'dep': DepDirective,
        'next': NextDirective,
        'showdeps': ShowDepsDirective,
        'shownexts': ShowNextsDirective,
    }
    indices = {
        # RecipeIndex,
        # IngredientIndex
    }
    initial_data = {
        # 'recipes': [],  # object list
        # 'recipe_ingredients': {},  # name -> object
    }

def DocReference(app, fromdocname, todocname, target=None):
    env = app.builder.env
    newnode = nodes.reference('', '')
    newnode['refdocname'] = todocname
    newnode['refuri'] = app.builder.get_relative_uri(fromdocname, todocname)
    if target is not None:
        newnode['refuri'] += '#' + target['refid']
    if todocname not in env.titles:
        raise SphinxError(f"No Document {todocname} in {fromdocname}")
    title = env.titles[todocname]
    newnode += nodes.inline(text=title.astext())
    return newnode

def process_guides(app, doctree, fromdocname):
    env = app.builder.env
    page_dep_list = {}
    page_next_list = {}

    for node_dep in doctree.traverse(dep):
        name = node_dep['title']
        if name not in page_dep_list:
            page_dep_list[name] = node_dep['targetid']

    for node_dep in doctree.traverse(next):
        name = node_dep['title']
        if name not in page_next_list:
            page_next_list[name] = node_dep['targetid']

    for node_lesson in doctree.traverse(showdeps):
        if len(page_dep_list) > 0:
            ul = nodes.bullet_list()
            for depname, deptargetid in page_dep_list.items():
                li = nodes.list_item()
                p = nodes.paragraph()
                ref = nodes.reference('', '')
                ref['refuri'] = '#' + deptargetid
                ref += nodes.inline(text=depname)
                p = nodes.paragraph()
                p+=ref
                li+=p
                ul+=li
            node_lesson += ul
        else:
            node_lesson.replace_self(nodes.comment(text="showdeps"))

    for node_lesson in doctree.traverse(shownexts):
        if len(page_next_list) > 0:
            ul = nodes.bullet_list()
            for depname, deptargetid in page_next_list.items():
                li = nodes.list_item()
                p = nodes.paragraph()
                ref = nodes.reference('', '')
                ref['refuri'] = '#' + deptargetid
                ref += nodes.inline(text=depname)
                p = nodes.paragraph()
                p+=ref
                li+=p
                ul+=li
            node_lesson += ul
        else:
            node_lesson.replace_self(nodes.comment(text="shownexts"))

def setup(app):
    DEBUG("GUIDE EXTENSION LOADED")
    app.add_domain(GuideDomain)
    app.connect('doctree-resolved', process_guides)
    app.add_node(showdeps,
                 html=(visit_deps, depart_deps),)
    app.add_node(shownexts,
                 html=(visit_shownexts, depart_shownexts),)
    app.add_node(dep,
                 html=(visit_dep, depart_dep),)
    app.add_node(next,
                 html=(visit_next, depart_next),)
    app.add_node(lesson,
                 html=(visit_lesson, depart_lesson),)
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
