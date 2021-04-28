from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective, directives

class youtube(nodes.General, nodes.Element):
    pass

def visit_youtube_node(self, node):
    self.body.append("""<div>""")
    self.body.append("""<div class="video-container">""")
    self.body.append(f"""<iframe src="{node['srcuri']}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>""")

def depart_youtube_node(self, node):
    self.body.append("""</div>""")
    self.body.append("""</div>""")

class youtubeDirective(SphinxDirective):
    required_arguments = 1
    option_spec = {    }

    def run(self):
        youtube_node = youtube()
        youtube_node['srcuri'] = self.arguments[0]

        return [youtube_node]

def setup(app):
    app.add_node(youtube,
                 html=(visit_youtube_node, depart_youtube_node),)
    app.add_directive('youtube', youtubeDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
