import os
import json
import uuid
import apiai


class Result:
    def __init__(self, error_msg, intent_name):
        self.error_msg = error_msg
        self.intent_name = intent_name

    def success(self):
        return self.error_msg == ''


class Parser(object):
    def __init__(self):
        cred_dir = os.path.join(os.path.expanduser('~'), '.config', 'credentials')
        if not os.path.exists(cred_dir):
            os.makedirs(cred_dir)
        self._config_file = os.path.join(cred_dir, 'apiai.json')
        self._session_id = ''
        self._lang = ''

    def create(self, lang):
        config = json.load(open(self._config_file, 'r'))
        self._ai = apiai.ApiAI(config['token'])
        self._session_id = str(uuid.uuid1())
        self._lang = lang

    def parse(self, text) -> Result:
        request = self._ai.text_request()
        request.lang = self._lang
        request.session_id = self._session_id
        request.query = text
        response = json.loads(request.getresponse().read())
        if response['status']['code'] != 200:
            return Result(response['status']['errorType'], '')

        result = response['result']
        if result['action'] == 'input.unknown':
            return Result(result['fulfillment']['speech'], '')

        return Result('', result['metadata']['intentName'])
