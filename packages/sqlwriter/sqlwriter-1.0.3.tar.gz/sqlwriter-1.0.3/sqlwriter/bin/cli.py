#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
from collections import namedtuple

from ..utils import db as db_utils
from ..utils.log.logging_mixin import LoggingMixin
from ..configuration import SUPPORTED_DATABASES

logger = logging.getLogger(__name__)


def initdb(args):
    logger.info('initializing databases: [%s]' % ', '.join(SUPPORTED_DATABASES))
    db_utils.initdb(args)
    logger.info("Done.")


Arg = namedtuple('Arg', ['flags', 'help', 'action', 'default', 'nargs', 'type', 'choices', 'metavar'])
Arg.__new__.__defaults__ = (None, None, None, None, None, None, None)


class CLIFactory(object):
    subparsers = (
        {
            'func': initdb,
            'help': "Initialize the metadata database",
            'args': tuple(),
        },
    )
    subparsers_dict = {sp['func'].__name__: sp for sp in subparsers}

    @classmethod
    def get_parser(cls, dag_parser=False):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
        subparsers.required = True

        subparser_list = cls.dag_subparsers if dag_parser else cls.subparsers_dict.keys()
        for sub in subparser_list:
            sub = cls.subparsers_dict[sub]
            sp = subparsers.add_parser(sub['func'].__name__, help=sub['help'])
            for arg in sub['args']:
                if 'dag_id' in arg and dag_parser:
                    continue
                arg = cls.args[arg]
                kwargs = {
                    f: getattr(arg, f)
                    for f in arg._fields if f != 'flags' and getattr(arg, f)}
                sp.add_argument(*arg.flags, **kwargs)
            sp.set_defaults(func=sub['func'])
        return parser


def get_parser():
    return CLIFactory.get_parser()
