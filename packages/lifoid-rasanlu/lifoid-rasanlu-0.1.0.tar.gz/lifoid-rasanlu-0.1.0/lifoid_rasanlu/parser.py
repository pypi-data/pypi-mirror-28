# -*- coding: utf8 -*-
"""
Rasa_nlu parserifoid
Author: Romary Dupuis <romary@me.com>
"""
import json
from requests import post
from lifoid.parser import Parser
from lifoid.config import settings


class RasaNluParser(Parser):
    def parse(self, message, _context):
        resp = post(settings.rasa_nlu.url, json={'q': message.text})
        output = None
        if resp.status_code == 200:
            json_response = json.loads(resp.content)
            self.logger.debug(json_response)
            output = json_response
        return output
