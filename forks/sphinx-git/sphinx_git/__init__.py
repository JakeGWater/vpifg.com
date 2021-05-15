# Copyright 2012-2013 (C) Daniel Watkins <daniel@daniel-watkins.co.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

import re
from datetime import datetime
from pathlib import Path

import six
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from git import Repo

import humanize

global SPHINX_SRC_DIR

# pylint: disable=too-few-public-methods, abstract-method
class GitDirectiveBase(Directive):
    def _find_repo(self):
        env = self.state.document.settings.env
        repo_dir = self.options.get('repo-dir', env.srcdir)
        repo = Repo(repo_dir, search_parent_directories=True)
        return repo


# pylint: disable=too-few-public-methods
class GitCommitDetail(GitDirectiveBase):
    default_sha_length = 7

    option_spec = {
        'branch': bool,
        'commit': bool,
        'uncommitted': bool,
        'untracked': bool,
        'sha_length': int,
        'no_github_link': bool,
    }

    # pylint: disable=attribute-defined-outside-init
    def run(self):
        self.repo = self._find_repo()
        self.branch_name = None
        if not self.repo.head.is_detached:
            self.branch_name = self.repo.head.ref.name
        self.commit = self.repo.commit()
        self.sha_length = self.options.get('sha_length',
                                           self.default_sha_length)
        markup = self._build_markup()
        return markup

    def _build_markup(self):
        field_list = nodes.field_list()
        item = nodes.paragraph()
        item.append(field_list)
        if 'branch' in self.options and self.branch_name is not None:
            name = nodes.field_name(text="Branch")
            body = nodes.field_body()
            body.append(nodes.emphasis(text=self.branch_name))
            field = nodes.field()
            field += [name, body]
            field_list.append(field)
        if 'commit' in self.options:
            name = nodes.field_name(text="Commit")
            body = nodes.field_body()
            if 'no_github_link' in self.options:
                body.append(self._commit_text_node())
            else:
                body.append(self._github_link())
            field = nodes.field()
            field += [name, body]
            field_list.append(field)
        if 'uncommitted' in self.options and self.repo.is_dirty():
            item.append(nodes.warning('', nodes.inline(
                text="There were uncommitted changes when this was compiled."
            )))
        if 'untracked' in self.options and self.repo.untracked_files:
            item.append(nodes.warning('', nodes.inline(
                text="There were untracked files when this was compiled."
            )))
        return [item]

    def _github_link(self):
        try:
            url = self.repo.remotes.origin.url
            url = url.replace('.git/', '').replace('.git', '')
            if 'github' in url:
                commit_url = url + '/commit/' + self.commit.hexsha
                ref = nodes.reference('', self.commit.hexsha[:self.sha_length],
                                      refuri=commit_url)
                par = nodes.paragraph('', '', ref)
                return par
            return self._commit_text_node()
        except AttributeError as error:
            print("ERROR: ", error)
            return self._commit_text_node()

    def _commit_text_node(self):
        return nodes.emphasis(text=self.commit.hexsha[:self.sha_length])


# pylint: disable=too-few-public-methods
class GitChangelog(GitDirectiveBase):

    option_spec = {
        'class': directives.unchanged,
        'revisions': directives.nonnegative_int,
        'rev-list': six.text_type,
        'detailed-message-pre': bool,
        'detailed-message-strong': bool,
        'filename_filter': six.text_type,
        'hide_author': bool,
        'hide_date': bool,
        'hide_details': bool,
        'repo-dir': six.text_type,
        'link-to-docs': bool,
        'title-exclude': six.text_type,
    }

    def run(self):
        if 'rev-list' in self.options and 'revisions' in self.options:
            self.state.document.reporter.warning(
                'Both rev-list and revisions options given; proceeding using'
                ' only rev-list.',
                line=self.lineno
            )
        commits = self._commits_to_display()
        markup = self._build_markup(commits)
        return markup

    def _get_files_in_commits(self, commits):
        commits_and_files = []
        for commit in commits:
            # SHA of an empty tree found at
            # http://stackoverflow.com/questions/33916648/get-the-diff-details-of-first-commit-in-gitpython
            # will be used to get the list of files of initial commit
            compared_with = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
            if len(commit.parents) > 0:  # pylint: disable=len-as-condition
                compared_with = commit.parents[0].hexsha
            files = []
            for diff in commit.diff(compared_with):
                files.append(diff.a_path)
                files.append(diff.b_path)
            commits_and_files.append((commit, files))
        return commits_and_files

    def _commits_to_display(self):
        repo = self._find_repo()
        commits = self._filter_commits(repo)
        return commits

    def _filter_commits(self, repo):
        if 'rev-list' in self.options:
            commits = repo.iter_commits(rev=self.options['rev-list'])
        else:
            commits = repo.iter_commits()
            revisions_to_display = 100
            commits = list(commits)[:revisions_to_display]
        # if 'filename_filter' in self.options:
        return self._filter_commits_on_filenames(commits)
        # return commits

    def _filter_commits_on_filenames(self, commits):
        filtered_commits = []
        filter_exp = re.compile(self.options.get('filename_filter', r'.*'))
        for commit in commits:
            # SHA of an empty tree found at
            # http://stackoverflow.com/questions/33916648/get-the-diff-details-of-first-commit-in-gitpython
            # will be used to get the list of files of initial commit
            compared_with = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
            if len(commit.parents) > 0:  # pylint: disable=len-as-condition
                compared_with = commit.parents[0].hexsha
            files = []
            for diff in commit.diff(compared_with):
                if 'filename_filter' in self.options:
                    # In the case of renames, we want the destination not the original
                    if filter_exp.match(diff.a_path):
                        files.append(diff.a_path)
                    # if filter_exp.match(diff.b_path):
                    #     files.append(diff.b_path)
                else:
                    files.append(diff.a_path)
                    files.append(diff.b_path)
            filtered_commits.append((commit, files))
        return filtered_commits

    def _build_markup(self, commits_and_files):
        global SPHINX_SRC_DIR
        output = output_node()
        list_node = nodes.bullet_list()
        i=0
        n = self.options.get('revisions', 100)
        for commit, files in commits_and_files:
            date_str = datetime.fromtimestamp(commit.authored_date)
            
            if 'title-exclude' in self.options:
                matcher = re.compile(self.options['title-exclude'], flags=re.IGNORECASE)
                if matcher.match(commit.message):
                    continue

            if i >= n: 
                break
            i = i + 1

            if '\n' in commit.message:
                message, detailed_message = commit.message.split('\n', 1)
            else:
                message = commit.message
                detailed_message = None
            
            files_ul = nodes.bullet_list()
            if SPHINX_SRC_DIR is not None and self.options.get('link-to-docs'):
                for file in list(dict.fromkeys(files)):
                    p = nodes.paragraph()
                    path = Path(SPHINX_SRC_DIR) / '..' / file
                    if os.path.exists(path):
                        text, _ = self.state.inline_text(':doc:`/%s`' % file[7:-4], lineno=-1)
                        p += text
                        # refuri = 'https://github.com/JakeGWater/vpifg.com/blob/%s/%s' % (commit.hexsha, file)
                        # file_link = nodes.reference('', commit.hexsha[0:8], refuri=refuri)
                    else:
                        refuri = 'https://github.com/JakeGWater/vpifg.com/blob/%s/%s' % (commit.hexsha, file)
                        file_link = nodes.reference('', file[7:], refuri=refuri)
                        p += file_link
                    list_item = nodes.list_item()
                    list_item.append(p)
                    files_ul.append(list_item)
            elif not self.options.get('hide_details'):
                for file in list(dict.fromkeys(files)):
                    # file_link = nodes.reference(text=file)
                    # file_link['refuri'] = "https://github.com/JakeGWater/vpifg.com/blob/%s/%s" % (commit.hexsha, file)
                    # print(file_link)
                    refuri = 'https://github.com/JakeGWater/vpifg.com/blob/%s/%s' % (commit.hexsha, file)
                    file_link = nodes.reference('', file[7:], refuri=refuri)
                    p = nodes.paragraph()
                    p += file_link
                    list_item = nodes.list_item()
                    list_item.append(p)
                    files_ul.append(list_item)

            item = nodes.list_item()
            par = nodes.paragraph()
            # search for PR numbers (e.g. #12)
            match = re.search(r'\#\d+', message)
            if match:
                span = match.span()
                begin = nodes.strong(text=message[:span[0]])
                pr_num = message[span[0]:span[1]]
                middle = nodes.reference(text=pr_num)
                middle['refuri'] = 'https://github.com/JakeGWater/vpifg.com/pull/%s' % pr_num[1:]
                end = nodes.strong(text=message[span[1]:])
                par += [begin, middle, end]
            else:
                par += nodes.strong(text=message)

            if not self.options.get('hide_author'):
                newnode = nodes.reference(commit.author.name, commit.author.name)
                newnode['refuri'] = 'https://github.com/%s' % commit.author.name
                par += [nodes.inline(text=" by "), newnode]
            if not self.options.get('hide_date'):
                par += [nodes.inline(text=" "), nodes.emphasis(text=humanize.naturaltime(date_str))]
            item.append(par)
            if detailed_message and not self.options.get('hide_details'):
                detailed_message = detailed_message.strip()
                if self.options.get('detailed-message-pre', False):
                    literal = nodes.literal_block(text=detailed_message)
                    literal['language'] = 'md'
                    item.append(literal)
                else:
                    item.append(nodes.paragraph(text=detailed_message))
            list_node.append(item)
            list_node.append(files_ul)
        output += list_node
        return [output]

class output_node(nodes.General, nodes.Element):
    pass

def html_visit_output_node(self, node):
    self.body.append(self.starttag(node, 'div', '', CLASS='gitlog'))

def html_depart_output_node(self, node):
    self.body.append('</div>')

def setup(app):
    global SPHINX_SRC_DIR
    
    SPHINX_SRC_DIR = app.srcdir
    app.add_node(
        output_node,
        html=(
            html_visit_output_node,
            html_depart_output_node
        )
    )
    app.add_directive('git_changelog', GitChangelog)
    app.add_directive('git_commit_detail', GitCommitDetail)
