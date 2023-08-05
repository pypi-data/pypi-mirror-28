# -*- coding: utf8 -*-
"""
Rasa_nlu plugin for Lifoid
Author: Romary Dupuis <romary@me.com>
"""
from lifoid import signals
from .config import RasanluConfiguration
from .parser import RasaNluParser

__version__ = '0.1.1'


def get_parser(app):
    return RasaNluParser()


def get_conf(configuration):
    setattr(configuration, 'rasa_nlu', RasanluConfiguration())


def register():
    signals.get_parser.connect(get_parser)
    signals.get_conf.connect(get_conf)
