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
from .. data_model import Table, Schemas
from . agent  import BaseAgent
from random import Random
from time import sleep

class BaseGenerator(BaseAgent):
    '''
    '''
    
class BatchGenerator(BaseGenerator):
    '''
    '''
    def __init__(self, batchSize=20, batchCount=-1, batchRate=1, seed=0):
        '''
        '''
        self.batchSize = batchSize
        self.batchRate = batchRate
        self.batchCount = batchCount
        self.seed = seed

        
    @property
    def random(self):
        try:
            return self._random
        except AttributeError:
            pass
        if self.seed:
            self._random = Random(self.seed)
        else:
            self._random = Random()
        return self._random

    
    @property
    def batchInterval(self):
        try:
            return self._batchInterval
        except AttributeError:
            pass
        try:
            self._batchInterval = 1./self.batchRate
        except ZeroDivisionError:
            self._batchInterval = 0
            
        return self._batchInterval

    
    @property
    def batchRange(self):
        '''
        '''
        return range(0, self.batchSize)    

    
    def batch(self):
        '''
        '''
        raise NotImplementedError()
        

    def run(self, func):
        '''
        '''
        count = self.batchCount
        while count != 0:
            count -= 1
            for item in self.batch():
                func(item)
            sleep(self.batchInterval)

            
class TransactionBatchGenerator(BatchGenerator):
    '''
    '''

    def __init__(self, path, rowFactoryName, payloadFactoryName, **kwds):
        '''
        '''
        super().__init__(**kwds)
        self.path = path
        self.rowFactoryName = rowFactoryName
        self.payloadFactoryName = payloadFactoryName

        
    @property
    def payloadFactory(self):
        try:
            return self._payloadFactory
        except AttributeError:
            pass
        factory = Schemas.transactionRequestFactory(self.payloadFactoryName)
        self._payloadFactory = factory
        return self._payloadFactory

    
    @property
    def table(self):
        try:
            return self._table
        except AttributeError:
            pass
        self._table = Table.withRowFactory(self.path,
                                           self.rowFactoryName,
                                           self.seed)
        return self._table
