#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Completion notes
1. Won't complete inside of a quote.  If there are mis-matched quotes
   it will break completions
2. terms upstream of a '(' are functions/modifiers
3. commas separate arguments of upstream function


"""

from typings import Mapping, Any

import bel.lang.fastparse as fastparse
import bel.lang.bel_specification as bel_specification

import logging
import logging.config

from bel.Config import config

# logging.config.dictConfig(config['logging'])
log = logging.getLogger(__name__)

default_bel = config['bel']['lang']['default_bel_version']


def cursor_arg(functions, cur_loc):
    """Find BEL argument at cursor location

    Args:
        functions (Mapping[str, Any]): dictionary of functions, args and spans
        cur_loc (int): given cursor location from input field

    Returns:
        (str, List[Mapping[str, Any]], int): function name, function arguments, argument index overlapping with cursor location
    """

    for key in functions:
        if cur_loc >= key[0] and cur_loc <= key[1]:
            function_name = functions[key]['name']
            args = functions[key]['args']
            for idx, arg in enumerate(functions[key]['args']):
                if cur_loc >= arg['span'][0] and cur_loc <= arg['span'][1]:
                    arg_idx = idx
                    return function_name, args, arg_idx

    return None, None, 0


def ns_completions(prefix, entity_types, tax_id):
    """Namespace completions
    """
    pass


def arg_completions(function, args, arg_idx, bel_version, bel_fmt, tax_id):
    """

    """

    bel_spec = bel_specification.get_client(version=bel_version)

    # positional arguments
    for args in bel_spec['function_signatures']['signatures']:

    return completions, function_help


def bel_completion(belstr: str, cur_loc: int = -1, bel_version: str = default_bel, bel_comp: str = None, bel_fmt: str = 'medium', tax_id: str = None) -> Mapping[str, Any]:
    """BEL Completion

    Args:
        belstr (str): BEL String to provide completion for
        cur_loc (int): cursor location - default of -1 means end of string
        bel_version (str): BEL Language version to use for completion
        bel_comp (str): ['subject', 'object', 'full', None] - a nested statement has to be found in object or full statement
        bel_fmt (str): ['short', 'medium', 'long'] BEL function/relation format
        tax_id (str): optional, species id is used to filter namespace values if applicable (e.g. Gene, RNA, ... entity_types)

    Returns:
        Mapping[str, Any]
    """

    functions, errors = fastparse.parse_function_string(belstr)
    spans, max_idx = fastparse.collect_spans(functions)
    function, args, arg_idx = cursor_arg(functions, cur_loc)
    completions, function_help = arg_completions(function, args, arg_idx, bel_version, bel_fmt, tax_id)

    return {'completions': completions, 'function_help': function_help, 'spans': spans}


def main():

    pass


if __name__ == '__main__':
    main()
