# -*- coding: utf8 -*-
"""
Google Translate plugin configuration
Author: Romary Dupuis <romary@me.com>
"""
from lifoid.config import Configuration, environ_setting


class GoogleTranslateConfiguration(Configuration):
    """
    Google Translate configuration
    """
    api_key = environ_setting('GOOGLE_TRANSLATE_API_KEY', '',
                              required=False)
