# Notes for Working with Docutils/Sphinx

* https://github.com/sphinx-doc/sphinx/blob/master/sphinx/writers/html5.py#L191
* https://github.com/docutils-mirror/docutils/
* https://github.com/docutils-mirror/docutils/blob/master/docutils/parsers/rst/states.py#L423
* Links are `nodes.reference(text=.., refuri=..)` _must_ be inside a text element like `nodes.paragraph()`
