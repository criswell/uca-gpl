'''
test_platform_id.py
-------------------

Tests the platform identification class from clientagent.common.platform_id
'''

import os
from clientagent.common.platform_id import PlatformID
import unittest

class TestPlatformID(unittest.TestCase):

    def setUp(self):
        self.platformID = PlatformID()

    def test_correctIsWindows(self):
        isWindows = False
        if os.name == 'nt':
            isWindows = True

        self.assertEqual(self.platformID.IS_WINDOWS, isWindows)

    def test_correctIsLinux(self):
        isLinux = True
        if os.name == 'nt':
            isLinux = False

        self.assertEqual(self.platformID.IS_LINUX, isLinux)

if __name__ == '__main__':
    unittest.main()

# vim:set ai et sts=4 sw=4 tw=80:
