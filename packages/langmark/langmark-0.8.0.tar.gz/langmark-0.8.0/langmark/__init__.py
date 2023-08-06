# Langmark - A powerful and extensible lightweight markup language.
# Copyright (C) 2015 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Langmark.
#
# Langmark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Langmark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Langmark.  If not, see <http://www.gnu.org/licenses/>.

from . import (metadata, base, factories, elements, headings, lists, code,
               formatting, links, quotes, html)


def P(*args, **kwargs):  # ***********************************************************
    import sys
    print(*args, file=sys.stderr, **kwargs)

# Additional extension modules should insert their meta element classes in the
#  list below; they must thus be imported *after* importing langmark, but
#  *before* instantiating the Langmark class
META_ELEMENTS = [metadata.Header,
                 links.LinksData]

# The order of the block element factories is important: put the most likey
#  elements first; some elements may rely on the fact that others have been
#  discarded
# Additional extension modules should insert their block-element factory
#  classes in the list below; they must thus be imported *after* importing
#  langmark, but *before* instantiating the Langmark class
BLOCK_FACTORIES = [# HeaderElements uninstalls itself after the first non-match
                   #  It also ensures that the content starts with an empty
                   #  line, thus making it possible to recognize elements that
                   #  start with an empty line (e.g. headings)
                   factories.HeaderElements(),
                   headings.HeadingElements(),
                   links.LinkDefinitions(),
                   # IndentedElements must come *after* factories that want to
                   #  ignore indentation (e.g. LinkDefinition), but *before*
                   #  factories whose elements might be inside indented blocks
                   factories.IndentedElements(),
                   code.CodeElements(),
                   lists.ListElements(),
                   quotes.QuoteElements(),
                   html.HTMLElements(),
                   factories.HorizontalRules()]

# The position of indented elements in the following list determines the level
#  of indentation needed to recognize them; the last element is also used for
#  greater indentation levels
# Additional extension modules should insert their indented element classes
#  in the list below; they must thus be imported *after* importing langmark,
#  but *before* instantiating the Langmark class
INDENTED_ELEMENTS = [None,
                     code.FormattableCodeBlockIndented,
                     code.PlainCodeBlockIndented,
                     elements.IndentedContainer]

# The order of the inline elements is instead not important
# Additional extension modules should insert their inline element classes in
#  the list below; they must thus be imported *after* importing langmark, but
#  *before* instantiating the Langmark class
INLINE_ELEMENTS = [formatting.Emphasis,
                   formatting.Strong,
                   formatting.Superscript,
                   formatting.Subscript,
                   formatting.Small,
                   formatting.Strikethrough,
                   links.Link,
                   code.FormattableCodeInline,
                   code.PlainCodeInline,
                   code.PlainTextInline,
                   # If line breaks are disabled, enable the DOTALL version of
                   #  base.Configuration.ESCAPE_RE
                   elements.LineBreak,
                   html.HTMLInlineTag]


class Langmark:
    def __init__(self):
        # The parameters for __init__ must reflect the attributes set through
        # argparse by the launcher script
        self.print_classes(elements._Element)  # ****************************************************
        elements._BlockElementContainingBlock.INSTALLED_BLOCK_FACTORIES = \
                                                                BLOCK_FACTORIES
        factories.IndentedElements.INSTALLED_ELEMENTS = INDENTED_ELEMENTS
        self.paragraph_factory = factories.ParagraphFactory()
        self._install_inline_elements()

    def _install_inline_elements(self):
        start_mark_to_element = {}
        element_to_compiled_mark = {}
        for Element in INLINE_ELEMENTS:
            mark = Element.INLINE_MARK
            start_mark_to_element[mark.start] = Element
            element_to_compiled_mark[Element] = mark.start
        # The first loop builds the dictionaries, which have to be installed
        #  in a separate loop
        for Element in element_to_compiled_mark:
            start_mark = element_to_compiled_mark[Element]
            Element.START_MARK_TO_INLINE_ELEMENT = start_mark_to_element.copy()
            del Element.START_MARK_TO_INLINE_ELEMENT[start_mark]
        elements.BaseInlineElement.START_MARK_TO_INLINE_ELEMENT = \
                                                start_mark_to_element.copy()

    def parse(self, stream):
        # The parameters for parse must reflect the attributes set through
        # argparse by the launcher script
        # TODO: Support passing a string instead of a stream
        self.stream = base.Stream(stream)
        for Meta in META_ELEMENTS:
            setattr(self, Meta.ATTRIBUTE_NAME, Meta(self))
        self.etree = elements.Root(self)
        self.etree.parse_tree()
        #self.print_subtree(self.etree)  # ********************************************************
        import sys  # ******************************************************************************
        print('META', self.header.keys, file=sys.stderr)  # *****************************************

    @staticmethod
    def print_subtree(element):
        # **********************************************************************************
        import sys
        root = element
        while True:
            if root.parent is not None:
                root = root.parent
            else:
                break
        def recurse(element, ind):
            print(ind, element, file=sys.stderr)
            ind += '  '
            try:
                children = element.children
            except AttributeError:
                pass
            else:
                for child in children:
                    recurse(child, ind)
        recurse(root, '')

    @staticmethod
    def print_classes(base_class):
        # **********************************************************************************
        import sys
        import inspect
        tree = inspect.getclasstree((class_[1] for class_ in
                            inspect.getmembers(elements, inspect.isclass) +
                            inspect.getmembers(metadata, inspect.isclass) +
                            inspect.getmembers(base, inspect.isclass) +
                            inspect.getmembers(headings, inspect.isclass) +
                            inspect.getmembers(lists, inspect.isclass) +
                            inspect.getmembers(code, inspect.isclass) +
                            inspect.getmembers(formatting, inspect.isclass) +
                            inspect.getmembers(links, inspect.isclass) +
                            inspect.getmembers(quotes, inspect.isclass) +
                            inspect.getmembers(html, inspect.isclass)))
        def recurse(tree, indent):
            if isinstance(tree, list):
                for node in tree:
                    recurse(node, indent + 1)
            else:
                print('    ' * indent, tree[0].__name__, file=sys.stderr)
        for i, node in enumerate(tree):
            if node[0] is base_class:
                print(base_class.__name__, file=sys.stderr)
                recurse(tree[i + 1], 0)
