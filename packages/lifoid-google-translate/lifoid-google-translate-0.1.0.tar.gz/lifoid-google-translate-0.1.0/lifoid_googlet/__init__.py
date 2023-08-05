# -*- coding: utf8 -*-
"""
Google Translate plugin for Lifoid
Author: Romary Dupuis <romary@me.com>
"""
from lifoid import signals
from .config import GoogleTranslateConfiguration
from .translator import GoogleTranslator

__version__ = '0.1.0'


def get_translator(app):
    return GoogleTranslator()


def get_conf(configuration):
    setattr(configuration, 'google_translate', GoogleTranslateConfiguration())


def register():
    signals.get_translator.connect(get_translator)
    signals.get_conf.connect(get_conf)
