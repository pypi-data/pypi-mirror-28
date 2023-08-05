import os.path
import sys
from lib2to3.pgen2 import token
from lib2to3 import pytree
from yapf.yapflib import pytree_unwrapper as w


def monkey_patch(cls):
    def _monkey_patch(method):
        setattr(cls, method.__name__, method)
        return method

    return _monkey_patch


@monkey_patch(w.PyTreeUnwrapper)
def Visit_import_from(self, node):
    for around_last in reversed(node.children):
        if around_last.type != token.COMMENT:
            break
    # node.type < 256 is maybe primitive token
    if around_last.type < 256 and around_last.value == ")":
        as_names = node.children[-2]
        if not as_names.children:
            # `from foo import (x)` to `from foo import (x,)`
            last_symbol = as_names
            parent = last_symbol.parent
            as_names = pytree.Node(298, [])
            parent.set_child(-2, as_names)
            as_names.append_child(last_symbol)
            as_names.append_child(pytree.Leaf(token.COMMA, ","))
        elif not hasattr(as_names.children[-1], "value") or as_names.children[-1].value != ",":
            # `from foo import (x, y)` to `from foo import (x, y,)`
            as_names.children.append(pytree.Leaf(token.COMMA, ","))

    self.DefaultNodeVisit(node)


@monkey_patch(w.PyTreeUnwrapper)
def Visit_import_as_names(self, node):
    """
    fix original yapf's bug. (with end of line comment is not supported)
    """
    prev = node.prev_sibling
    while prev.type == token.COMMENT:
        prev = prev.prev_sibling
    if prev.value == '(':
        w._DetermineMustSplitAnnotation(node)
    self.DefaultNodeVisit(node)


STYLE = """\
[style]
based_on_style = pep8
column_limit = 100
dedent_closing_brackets=true
spaces_around_power_operator = true
split_arguments_when_comma_terminated = true
join_multiple_lines = false\
"""


def main():
    stylepath = os.path.join(os.environ.get("HOME"), ".config/yapf/style")
    if not os.path.exists(stylepath):
        os.makedirs(os.path.dirname(stylepath), exist_ok=True)
        print("{path} is not found, ... created".format(path=stylepath), file=sys.stderr)

        with open(stylepath, "w") as wf:
            wf.write(STYLE)

    import yapf
    yapf.run_main()


if __name__ == "__main__":
    main()
