# -*- coding: utf-8 -*-
# 
# The MIT License (MIT)
# 
# Copyright (c) 2016 Ivo Tzvetkov
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

from __future__ import print_function, unicode_literals
import json

class Output(object):

    def __init__(self, config):
        self.match = config.get('match', [])

    def send(self, target, data):
        if self.match:
            for match in self.match:
                matched = True
                for k in match:
                    if data.get(k) != match[k]:
                        matched = False
                        break
                if matched:
                    return self._send(target, data)
        else:
            return self._send(target, data)

    def _send(self, target, data):
        raise NotImplementedError()

class UDPLoggerOutput(Output):

    def __init__(self, config):
        super(UDPLoggerOutput, self).__init__(config)
        from udplogger.client import Client
        self.client = Client(host=config['host'],
                             port=config['port'])

    def _send(self, target, data):
        self.client.send(table=target, data=data)

class RedMsgOutput(Output):

    def __init__(self, config):
        super(RedMsgOutput, self).__init__(config)
        from redmsg import Publisher
        self.client = Publisher(host=config['host'],
                                port=config['port'],
                                db=config['db'],
                                ttl=config.get('ttl', 3600))

    def _send(self, target, data):
        self.client.publish(target, json.dumps(data))

OUTPUTS = {
    'udplogger': UDPLoggerOutput,
    'redmsg': RedMsgOutput,
}

def create_output(config):
    return OUTPUTS[config['type']](config)
