# -*- coding: utf8 -*-
"""
Dialogflow plugin for Lifoid
Author: Romary Dupuis <romary@me.com>
"""
from lifoid import signals
from lifoid.config import settings
from .config import DialogflowConfiguration
from .parser import DialogflowParser

__version__ = '0.1.0'


def get_parser(app):
    return DialogflowParser(settings.dialogflow.access_token)


def get_conf(configuration):
    setattr(configuration, 'dialogflow', DialogflowConfiguration())


def register():
    signals.get_parser.connect(get_parser)
    signals.get_conf.connect(get_conf)
