"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import logging
import requests

from programy.services.service import Service
from programy.config.sections.brain.service import BrainServiceConfiguration


class RestAPI(object):

    def get(self, host, data):
        return requests.get(host, data=data)

    def post(self, host, data):
        return requests.post(host, data=data)


class GenericRESTService(Service):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = RestAPI()
        else:
            self.api = api

        self.payload = {}

        if config.method is None:
            self.method = "GET"
        else:
            self.method = config.method

        if config.host is None:
            raise Exception("Undefined host parameter")
        self.host = config.host

    def ask_question(self, bot, clientid: str, question: str):

        try:
            if self.method == 'GET':
                response = self.api.get(self.host, data=self.payload)
            elif self.method == 'POST':
                response = self.api.post(self.host, data=self.payload)
            else:
                raise Exception("Unsupported REST method [%s]"%self.method)

            if response.status_code != 200:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("[%s] return status code [%d]", self.host, response.status_code)
            else:
                return response.text

        except Exception as excep:
            logging.exception(excep)

        return ""
