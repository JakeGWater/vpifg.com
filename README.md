# VPIFG

> Source files and content for https://vpifg.com

# Contribute

There are three primary ways to contribute:

1. [Edit directly on the website](#edit-on-website) _(Easiest)_.
2. [Edit using Gitpod](#edit-in-gitpod) _(Easy and you get to see a local preview)_.
3. [Local checkout](#local-checkout).

In all cases, you will have to:

1. Follow the [Contribution Guidelines](https://github.com/JakeGWater/vpifg.com/blob/main/source/about/contributing.rst) 
1. [Create a Pull-Request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)
1. Sign the [CLA](#cla)*
1. Respond to any feedback, and wait for merge.

Once the PR is merged, it will immediately be live.

## Edit on Website

See [Editing files in your repository
](https://docs.github.com/en/github/managing-files-in-a-repository/editing-files-in-your-repository).

Example: [Edit this file](https://github.com/JakeGWater/vpifg.com/edit/main/README.md)

## Edit in Gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/JakeGWater/vpifg.com)

Gitpod will bootstrap a cloud dev environment for you.
It is temporary, so push your changes regularly, but everything will be setup out of the box.
You can even preview your ideas live.

## Local Checkout

### Pre-Requisites

1. Git must be installed
1. Python 3.8.9 or greater 

### Install

```sh
$ git clone https://github.com/JakeGWater/vpifg.com
$ cd vpifg.com
$ pip3 install -r requirements.txt
```

### Develop

```sh
npm start
```

_You do not need npm, it is for convenience only. Check out the package.json file for the direct python commands to run_.

View your site at http://localhost:3000/

# Architecture

1. We use [Sphinx](https://github.com/sphinx-doc/sphinx) to build a static html site using,
   [docutils](https://docutils.sourceforge.io/) and [reStructuredText](https://docutils.sourceforge.io/rst.html).
1. We use a modified [Pydata Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme).
1. Pull-requests are tested using a [GitHub Test Action](https://github.com/JakeGWater/vpifg.com/blob/main/.github/workflows/test.yaml).
1. [CLA Assistant](https://cla-assistant.io/) handles the CLAs.
1. On merging to `main` we use a [GitHub Build Action](https://github.com/JakeGWater/vpifg.com/blob/main/.github/workflows/main.yml) to deploy a `gh-pages` branch.
1. GitHub Pages hosts the static site.
1. Cloudflare provides a CDN.

The above architecture currently has zero reocurring costs, aside from the domain name.

# License

All content in `source` is licensed according to [`source/LICENSE.md`](source/LICENSE.md),
unless otherwise specified in `source/about/licenses.rst` or as noted within the file.

All content outside of `source` is licensed under its original licenses,
or licensed as [MIT](https://opensource.org/licenses/MIT) as a fallback.

# CLA

See https://vpifg.com/cla
