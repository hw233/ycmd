#
# Copyright (C) 2015 ycmd contributors
#
# This file is part of ycmd.
#
# ycmd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ycmd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ycmd.  If not, see <http://www.gnu.org/licenses/>.

from ycmd.server_utils import SetUpPythonPath
SetUpPythonPath()

import bottle, httplib, os

from nose.tools import with_setup
from hamcrest import ( contains,
                       contains_inanyorder,
                       empty,
                       has_entries )

from ycmd.tests.test_utils import Setup
from ycmd.tests.get_completions_test import ( CompletionEntryMatcher,
                                              GetCompletions_RunTest )

from .test_utils import ( TEST_DATA_DIR,
                          PathToTestFile,
                          StopTernServer,
                          with_cwd,
                          WaitForTernServerReady  )

bottle.debug( True )

# The following properties/methods are in Object.prototype, so are present
# on all objects:
#
# toString()
# toLocaleString()
# valueOf()
# hasOwnProperty()
# propertyIsEnumerable()
# isPrototypeOf()
#

@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Works_NoQuery_test():
  GetCompletions_RunTest( {
    'description': 'semantic completion works for simple object no query',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'simple_test.js' ),
      'line_num':   13,
      'column_num': 43,
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains_inanyorder(
          CompletionEntryMatcher( 'a_simple_function',
                                  'fn(param: ?) -> string' ),
          CompletionEntryMatcher( 'basic_type', 'number' ),
          CompletionEntryMatcher( 'object', 'object' ),
          CompletionEntryMatcher( 'toString', 'fn() -> string' ),
          CompletionEntryMatcher( 'toLocaleString', 'fn() -> string' ),
          CompletionEntryMatcher( 'valueOf', 'fn() -> number' ),
          CompletionEntryMatcher( 'hasOwnProperty',
                                  'fn(prop: string) -> bool' ),
          CompletionEntryMatcher( 'isPrototypeOf', 'fn(obj: ?) -> bool' ),
          CompletionEntryMatcher( 'propertyIsEnumerable',
                                  'fn(prop: string) -> bool' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer )


@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Works_Query_test():
  GetCompletions_RunTest( {
    'description': 'semantic completion works for simple object with query',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'simple_test.js' ),
      'line_num':   14,
      'column_num': 45,
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains(
          CompletionEntryMatcher( 'basic_type', 'number' ),
          CompletionEntryMatcher( 'isPrototypeOf', 'fn(obj: ?) -> bool' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer  )


@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Works_Require_NoQuery_test():
  GetCompletions_RunTest( {
    'description': 'semantic completion works for simple object no query',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'requirejs_test.js' ),
      'line_num':   2,
      'column_num': 15,
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains_inanyorder(
          CompletionEntryMatcher( 'mine_bitcoin', 'fn(how_much: ?) -> number' ),
          CompletionEntryMatcher( 'get_number', 'number' ),
          CompletionEntryMatcher( 'get_string', 'string' ),
          CompletionEntryMatcher( 'get_thing', 'fn(a: ?) -> number|string' ),
          CompletionEntryMatcher( 'toString', 'fn() -> string' ),
          CompletionEntryMatcher( 'toLocaleString', 'fn() -> string' ),
          CompletionEntryMatcher( 'valueOf', 'fn() -> number' ),
          CompletionEntryMatcher( 'hasOwnProperty',
                                  'fn(prop: string) -> bool' ),
          CompletionEntryMatcher( 'isPrototypeOf', 'fn(obj: ?) -> bool' ),
          CompletionEntryMatcher( 'propertyIsEnumerable',
                                  'fn(prop: string) -> bool' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer  )


@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Works_Require_Query_test():
  GetCompletions_RunTest( {
    'description': 'semantic completion works for require object with query',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'requirejs_test.js' ),
      'line_num':   3,
      'column_num': 17,
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains(
          CompletionEntryMatcher( 'mine_bitcoin', 'fn(how_much: ?) -> number' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer  )


@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Works_Require_Query_LCS_test():
  GetCompletions_RunTest( {
    'description': 'completion works for require object with query not prefix',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'requirejs_test.js' ),
      'line_num':   4,
      'column_num': 17,
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains(
          CompletionEntryMatcher( 'get_number', 'number' ),
          CompletionEntryMatcher( 'get_thing', 'fn(a: ?) -> number|string' ),
          CompletionEntryMatcher( 'get_string', 'string' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer  )


@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Dirty_Named_Buffers_test():
  # This tests that when we have dirty buffers in our editor, tern actually uses
  # them correctly
  GetCompletions_RunTest( {
    'description': 'completion works for require object with query not prefix',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'requirejs_test.js' ),
      'line_num':   18,
      'column_num': 11,
      'file_data': {
        os.path.join( TEST_DATA_DIR, 'no_such_lib', 'no_such_file.js' ): {
          'contents': (
            'define( [], function() { return { big_endian_node: 1 } } )') ,
          'filetypes': [ 'javascript' ]
        }
      },
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains_inanyorder(
          CompletionEntryMatcher( 'big_endian_node', 'number' ),
          CompletionEntryMatcher( 'toString', 'fn() -> string' ),
          CompletionEntryMatcher( 'toLocaleString', 'fn() -> string' ),
          CompletionEntryMatcher( 'valueOf', 'fn() -> number' ),
          CompletionEntryMatcher( 'hasOwnProperty',
                                  'fn(prop: string) -> bool' ),
          CompletionEntryMatcher( 'isPrototypeOf', 'fn(obj: ?) -> bool' ),
          CompletionEntryMatcher( 'propertyIsEnumerable',
                                  'fn(prop: string) -> bool' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer  )


@with_setup( Setup )
@with_cwd( TEST_DATA_DIR )
def GetCompletions_TernCompleter_Returns_Docs_In_Completions_test():
  # This tests that we supply docs for completions
  GetCompletions_RunTest( {
    'description': 'completions supply docs',
    'request': {
      'filetype':   'javascript',
      'filepath':   PathToTestFile( 'requirejs_test.js' ),
      'line_num':   8,
      'column_num': 15,
    },
    'expect': {
      'response': httplib.OK,
      'data': has_entries( {
        'completions': contains_inanyorder(
          CompletionEntryMatcher( 'a_function',
                                  'fn(bar: ?) -> {a_value: string}', {
            'detailed_info': ('fn(bar: ?) -> {a_value: string}\n'
                           + 'This is a short documentation string'),
          } ),
          CompletionEntryMatcher( 'options', 'options' ),
          CompletionEntryMatcher( 'toString', 'fn() -> string' ),
          CompletionEntryMatcher( 'toLocaleString', 'fn() -> string' ),
          CompletionEntryMatcher( 'valueOf', 'fn() -> number' ),
          CompletionEntryMatcher( 'hasOwnProperty',
                                  'fn(prop: string) -> bool' ),
          CompletionEntryMatcher( 'isPrototypeOf', 'fn(obj: ?) -> bool' ),
          CompletionEntryMatcher( 'propertyIsEnumerable',
                                  'fn(prop: string) -> bool' ),
        ),
        'errors': empty(),
      } )
    },
  }, WaitForTernServerReady, StopTernServer  )