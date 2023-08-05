#   Copyright 2017 Intel, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import mock
import testtools

from rsdclient.common import command


class CommandTest(testtools.TestCase):

    def test__split_lines(self):
        formatter = command._SmartHelpFormatter(mock.Mock())

        # Test format message with newline
        result = formatter._split_lines("a\n\nb\nc", 1)
        expected = ["a", "", "b", "c"]
        self.assertEqual(result, expected)

        # Test format message with heading whitespaces
        result = formatter._split_lines("  ab", 3)
        expected = ["  a", "  b"]
        self.assertEqual(result, expected)
