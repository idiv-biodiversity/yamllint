# -*- coding: utf-8 -*-
# Copyright (C) 2016 Adrien Vergé
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to require or forbid the use of document start marker (``---``).

.. rubric:: Options

* Set ``present`` to ``true`` when the document start marker is required, or to
  ``false`` when it is forbidden.
* ``min-empty-lines-after`` defines the minimal number of empty lines after the
  document start marker.
* ``max-empty-lines-after`` defines the maximal number of empty lines after the
  document start marker.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   document-start:
     present: true

.. rubric:: Examples

#. With ``document-start: {present: true}``

   the following code snippet would **PASS**:
   ::

    ---
    this:
      is: [a, document]
    ---
    - this
    - is: another one

   the following code snippet would **FAIL**:
   ::

    this:
      is: [a, document]
    ---
    - this
    - is: another one

#. With ``document-start: {present: false}``

   the following code snippet would **PASS**:
   ::

    this:
      is: [a, document]
    ...

   the following code snippet would **FAIL**:
   ::

    ---
    this:
      is: [a, document]
    ...
"""


import yaml

from yamllint.linter import LintProblem


ID = 'document-start'
TYPE = 'token'
CONF = {'present': bool,
        'max-empty-lines-after': int,
        'min-empty-lines-after': int}
DEFAULT = {'present': True,
           'max-empty-lines-after': -1,
           'min-empty-lines-after': 0}


def check(conf, token, prev, next, nextnext, context):
    if conf['present']:
        if (isinstance(prev, (yaml.StreamStartToken,
                              yaml.DocumentEndToken,
                              yaml.DirectiveToken)) and
            not isinstance(token, (yaml.DocumentStartToken,
                                   yaml.DirectiveToken,
                                   yaml.StreamEndToken))):
            yield LintProblem(token.start_mark.line + 1, 1,
                              'missing document start "---"')

        if isinstance(prev, yaml.DocumentStartToken):
            empty_lines = token.start_mark.line - prev.start_mark.line - 1

            if (conf['max-empty-lines-after'] >= 0 and
                    empty_lines > conf['max-empty-lines-after']):
                yield LintProblem(token.start_mark.line + 1,
                                  token.start_mark.column + 1,
                                  'too many empty lines after document start')

            if (conf['min-empty-lines-after'] > 0 and
                    empty_lines < conf['min-empty-lines-after']):
                yield LintProblem(token.start_mark.line + 1,
                                  token.start_mark.column + 1,
                                  'too few empty lines after document start')

    else:
        if isinstance(token, yaml.DocumentStartToken):
            yield LintProblem(token.start_mark.line + 1,
                              token.start_mark.column + 1,
                              'found forbidden document start "---"')
