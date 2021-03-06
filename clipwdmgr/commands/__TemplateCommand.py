# -*- coding: utf-8 -*-

#The MIT License (MIT)
#
#Copyright (c) 2015,2018 Sami Salkosuo
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
#template for commands - copy this to new file and rename and change this description
#

from ..utils.utils import *
from ..utils.functions import *
from ..database.database import *
from ..utils.settings import Settings
from .SuperCommand import *
from ..globals import *
from ..globals import GlobalVariables

class __TemplateCommand(SuperCommand):

    def __init__(self,cmd_handler):
        super().__init__(cmd_handler)
    
    
    def parseCommandArgs(self,userInputList):
        #implement in command class
        #parse arguments like in this method
        cmd_parser = ThrowingArgumentParser(prog="uname",description='Generate random username using given format.')
        cmd_parser.add_argument('-t','--total',metavar='NR', required=False, type=int, default=1, help='Total number of usernames to generate.')
        cmd_parser.add_argument('format',metavar='FORMAT', type=str, nargs='?', default="CVCCVC", help='Username format: C=consonant, V=vowel, N=number, +=space. Default is: CVCCVC.')

        (self.cmd_args,self.help_text)=parseCommandArgs(cmd_parser,userInputList)

    def execute(self):

        #implement command here

        formatStr=self.cmd_args.format
        N=self.cmd_args.total
        for i in range(N):
            pwd=generate_username(formatStr,False)
            print(pwd)

