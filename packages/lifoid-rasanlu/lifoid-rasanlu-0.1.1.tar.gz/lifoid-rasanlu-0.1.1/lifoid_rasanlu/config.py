# -*- coding: utf8 -*-
"""
Rasa_nlu plugin configuration
Author: Romary Dupuis <romary@me.com>
"""
from lifoid.config import Configuration, environ_setting


class RasanluConfiguration(Configuration):
    """
    Rasa_nlu configuration
    """
    url = environ_setting('RASANLU_URL', 'http://127.0.0.1:5000/parse',
                          required=False)
