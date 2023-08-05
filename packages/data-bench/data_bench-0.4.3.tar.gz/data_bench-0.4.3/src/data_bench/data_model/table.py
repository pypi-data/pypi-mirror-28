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

from pathlib import Path
from .schemas import Schemas
import random

class Table(object):
    '''
    '''

    @classmethod
    def withRowFactory(cls, path, rowFactoryName, seed=0, sep='|'):
        table = cls(path, seed, sep)
        table.rowFactory = Schemas.tableRowFactory(rowFactoryName)
        return table

    
    def __init__(self, path, seed=0, sep='|'):
        '''
        '''
        self.path = Path(path)
        self.sep = str(sep)
        self.seed = int(seed)

        
    def __iter__(self):
        return iter(self.rows)

    
    def __str__(self):
        s = []
        for r in self.rows:
            s.append(self.sep.join([getattr(r,x) for x in r._fields]))
        return '\n'.join(s)


    @property
    def random(self):
        try:
            return self._random
        except AttributeError:
            pass
        if self.seed:
            self._random = random.Random(self.seed)
        else:
            self._random = random.Random()
        return self._random

    
    @property
    def rows(self):
        '''
        '''
        try:
            return self._rows
        except AttributeError:
            pass
        valid = lambda r: len(r) > 0
        self._rows = []
        with self.path.open() as f:
            for line in f:
                if not valid(line):
                    continue
                args = line.strip().split(self.sep)
                self._rows.append(self.rowFactory(*args))
        return self._rows

        
    def pick(self, count=1):
        '''
        '''

        if count <= 0:
            return []
        
        return self.random.sample(self.rows, count)


    def shuffle(self):
        '''
        '''
        self.random.shuffle(self.rows)

        return self

    
    def unshuffle(self):
        '''
        Unshuffle effected by deleting and re-reading the data from
        the source file. Changes to the data are lost.
        '''
        del(self._rows)
        
        return self

    
    def rowMatching(self, column_name, value, cmpf=None):
        '''
        '''

        try:
            return [x for x in self.rows if getattr(x,column_name) == value][0]
        except KeyError:
            raise ValueError(f'{value} not found')

        values = [getattr(x, column_name) for x in self.rows]
        return self.rows[values.index(value)]


        
        

        




        
    
        
