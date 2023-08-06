import inspect
import importlib

from textwrap import dedent


SEPARATOR = '::'


def resolve(string):
    if SEPARATOR not in string:
        return importlib.import_module(string)
    module_name, member_name = string.split(SEPARATOR)
    module = importlib.import_module(module_name)
    if member_name:
        return getattr(module, member_name)
    else:
        return module


def render(node):
    if inspect.ismodule(node):
        return render_module(node)
    elif inspect.isclass(node):
        return render_class(node)
    elif inspect.isfunction(node):
        return render_function(node)


def render_module(node):
    if not node.__doc__:
        return ''
    return dedent('''\
    ## {name}

    {doc}
    ''').format(name=node.__name__, doc=dedent(node.__doc__.strip()))


def render_class(node):
    if not node.__doc__:
        return ''
    out = dedent('''\
    ### {name}

    {doc}
    ''').format(name=node.__name__, doc=dedent(node.__doc__.strip()))

    for name, method in inspect.getmembers(node, _is_method):
        if not method.__doc__:
            continue
        out += '\n'
        out += dedent('''\
        #### {name}

        {doc}
        ''').format(name=name, doc=dedent(method.__doc__.strip()))
    return out


def render_method(node):
    pass


def render_function(node):
    if not node.__doc__:
        return ''
    return dedent('''\
    ### {name}

    {doc}
    ''').format(name=node.__name__, doc=dedent(node.__doc__.strip()))


def parse(spec):
    node = resolve(spec.strip())
    return render(node)
    # return spec


def _is_method(node):
    return inspect.isfunction(node) or inspect.ismethod(node)
