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

from argparse import ArgumentParser, Namespace
from configparser import ConfigParser

class CLIGenerator(object):
    '''
    '''

    @classmethod
    def parseArgumentsFor(cls, arguments):
        '''Returns an argparse.Namespace populated with arguments
        found on the command-line.

        arguments:      dict -> key is argument string specifier, 
                                value is a dictionary of add_argument options

        XXX Example

        '''
        return cls(arguments).parse_args()
    

    def __init__(self, arguments):
        '''
        arguments:        dict
        '''
        for k,v in arguments.items():
            self.parser.add_argument(k, **v)
        
    @property
    def parser(self):
        '''An argparse.ArgumentParser()
        '''
        try:
            return self._parser
        except AttributeError:
            pass
        self._parser = ArgumentParser()
        return self._parser

    def parse_args(self):
        '''
        Returns an argparse.Namespace configured with command-line
        arguments.
        '''
        
        return self.parser.parse_args()

