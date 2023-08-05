#
#   Copyright 2017 Intel Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#    
'''
'''

from uuid import uuid4
import time

class Transaction(object):
    '''
    '''
    _sequence = 0

    @classmethod
    def parse(self, content, sep='|'):
        '''
        '''
        raise NotImplementedError()
        
    
    def __init__(self, payload, sep='|'):
        '''
        payload - instance of a class created from namedtuple
        sep     - optional string value 

        '''
        self.payload = payload
        self.sep = sep


    def __repr__(self):
        '''
        '''
        payload_class = self.payload.__class__.__name__
        return '{}(payload={}, sep={!r})'.format(self.__class__.__name__,
                                                 payload_class,
                                                 self.sep)

    def __str__(self):
        '''
        '''
        fields = [self.payload.__class__.__name__,
                  str(self.uuid),
                  str(self.timestamp),
                  str(self.sequence)]
        for field in self.payload._fields:
            fields.append(str(getattr(self.payload, field)))
        return self.sep.join(fields)


    @property
    def uuid(self):
        '''
        Returns a uuid.uuid4().
        '''
        try:
            return self._uuid
        except AttributeError:
            pass
        self._uuid = uuid4()
        return self._uuid

    @property
    def timestamp(self):
        '''
        Epoch timestamp in nanoseconds.
        '''
        return int(time.time() * 1e9)

    
    @property
    def sequence(self):
        '''
        An integer assigned to each Transaction instance which
        is monotonic and increasing.
        '''
        Transaction._sequence += 1
        return Transaction._sequence




