import json
import uuid
import apiai


class Result(object):
    def __init__(self, intent_name, parameters):
        self.intent_name = intent_name
        self.parameters = parameters


class Parser(object):
    def __init__(self):
        self._session_id = ''
        self._lang = ''
        self._empty = Result('', '')

    def create(self, config):
        self._ai = apiai.ApiAI(config['token'])
        self._session_id = str(uuid.uuid1())
        self._lang = config['lang']

    def parse(self, text) -> (str, Result):
        request = self._ai.text_request()
        request.lang = self._lang
        request.session_id = self._session_id
        request.query = text
        request.time_zone = 'Europe/Moscow'
        response = json.loads(request.getresponse().read())
        if response['status']['code'] != 200:
            err = 'api.ai error: {}'.format(response['status']['errorType'])
            return err, self._empty

        result = response['result']
        if result['action'] == 'input.unknown':
            err = result['fulfillment']['speech']
            return err, self._empty

        err = ''
        return err, Result(result['metadata']['intentName'], result['parameters'])
