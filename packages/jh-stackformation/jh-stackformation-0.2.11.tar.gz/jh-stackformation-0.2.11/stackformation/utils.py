import jinja2
import re
import imp
import os
from troposphere import Parameter
import click
from colorama import Fore, Style, Back  # noqa


def jinja_env(context, capture_vars=False):

    var_capture = []

    def _handle_context(var):
        if capture_vars:
            var_capture.append(var)
        else:
            if context.check_var(var):
                return context.get_var(var)
            raise Exception("Context Error: Output Missing ({})".format(var))

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))

    env.globals['context'] = _handle_context

    return env, var_capture


def match_stack(selector, stack):
    """Match stacks using selector as the comparison var.
    Strings prefixed with ^ will be treated as negative

    Args:
        selector (str|list[str]): String tokens or list used for matching
        stack (:obj:`stackformation.BaseStack`): stack used for comparison. Will match on get_stack_name() and get_remote_stack_name()

    Returns:
        :obj:`stackformation.BaseStack`: If stack matches
        bool: False if selector did not match
    """  # noqa
    if not isinstance(selector, list):
        selector = selector.split(' ')

    selector = [i.lower() for i in selector]

    pos = []
    neg = []
    sn = stack.get_stack_name().lower()
    rn = stack.get_remote_stack_name().lower()
    result = False

    for s in selector:
        if s[0] == "^":
            neg.append(s[1:])
        else:
            pos.append(s)

    for s in pos:
        if (s in sn) or (s in rn):
            result = True

    for s in neg:
        if (s in sn) or (s in rn):
            result = False

    return result


def match_image(selector, image_name):

    if not isinstance(selector, list):
        selector = selector.split(' ')

    selector = [i.lower() for i in selector]

    pos = []
    neg = []
    result = False
    im = image_name.lower()

    for s in selector:
        if s[0] == "^":
            neg.append(s[1:])
        else:
            pos.append(s)

    result = False

    for s in pos:
        if s in im:
            result = True

    for s in neg:
        if s in im:
            result = False

    return result


def ucfirst(word):
    """Uppercase the first letter in a string
    and error if string starts with an digit

    Args:
        word (str): the word

    Raises:
        Exception

    Returns:
        (str)

    """
    if len(word) <= 0:
        return ""
    if not re.match('^[a-zA-Z]', word):
        raise Exception("{} Cannot begin with a digit".format(word))
    ls = list(word)
    ls[0] = ls[0].upper()
    return ''.join(ls)


def tparam(template, name, value, description, default=None):

    p = template.add_parameter(Parameter(
        name,
        Type='String',
        Description=description
    ))

    if default:
        p.Default = default

    return p


def load_infra_module(infra_file):

    try:

        module = imp.load_source('deploy', infra_file)

    except Exception as e:
        click.echo("Infra file ({}) not found!".format(infra_file))
        exit(1)

    return module


def template_env(path):

    path = os.path.dirname(os.path.realpath(__file__))

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            searchpath=path))

    return env


def color_index(index):

    colors = {
            'cf_status': {
                'CREATE_IN_PROGRESS': Fore.YELLOW,
                'CREATE_FAILED': Fore.RED,
                'CREATE_COMPLETE': Fore.GREEN,
                'ROLLBACK_IN_PROGRESS': Fore.RED,
                'ROLLBACK_FAILED': Fore.RED,
                'ROLLBACK_COMPLETE': Fore.RED,
                'DELETE_IN_PROGRESS': Fore.YELLOW,
                'DELETE_FAILED': Fore.RED,
                'DELETE_COMPLETE': Fore.GREEN,
                'UPDATE_FAILED': Fore.RED,
                'UPDATE_IN_PROGRESS': Fore.YELLOW,
                'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS': Fore.YELLOW,
                'UPDATE_COMPLETE': Fore.GREEN,
                'UPDATE_ROLLBACK_IN_PROGRESS': Fore.RED,
                'UPDATE_ROLLBACK_FAILED': Fore.RED,
                'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS': Fore.YELLOW,
                'UPDATE_ROLLBACK_COMPLETE': Fore.GREEN,
            }
        } # noqa

    return colors[index]
