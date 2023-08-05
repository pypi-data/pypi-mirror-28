# -*- coding: utf8 -*-
"""
Dialogflow plugin ocnfiguration
Author: Romary Dupuis <romary@me.com>
"""
from lifoid.config import Configuration, environ_setting


class DialogflowConfiguration(Configuration):
    """
    Configuration for the web server to run an admin UI.
    """
    access_token = environ_setting('DIALOGF_ACCESS_TOKEN', '',
                                   required=True)
    dev_access_token = environ_setting('DIALOGF_DEV_ACCESS_TOKEN',
                                       '', required=False)
