# -*- coding: utf8 -*-
"""
Dialogflow parser
Author: Romary Dupuis <romary@me.com>
"""
import os
import binascii
import json
from apiai import ApiAI
from awesomedecorators import memoized
from lifoid.parser import Parser

SESSID_LENGTH = 12


class DialogflowParser(Parser):
    """
    Dialogflow parser
    """
    def __init__(self, access_token):
        self.access_token = access_token

    @memoized
    def dialogflow(self):
        """
        Dialogflow connexion
        """
        self.logger.debug('Initialize parser')
        return ApiAI(self.access_token)

    def parse(self, message, _context):
        """
        Implementation of generic parser method
        """
        request = self.dialogflow.text_request()
        request.query = message
        request.resetContexts = True
        request.contexts = []
        request.session_id = str(
            binascii.hexlify(os.urandom(SESSID_LENGTH)))
        response = request.getresponse()
        json_response = json.loads(response.read())
        self.logger.debug(json_response)
        if json_response['status']['code'] == 200:
            return {
                'result': json_response,
                'intent': json_response['result']['action'],
                'entities': json_response['result'].get('parameters', []),
                'speech': json_response['result']
                .get('fulfillment', {'speech': ''})['speech']
            }
        else:
            return None
