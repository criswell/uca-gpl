'''
test_platform_id.py
-------------------

Tests the platform identification class from clientagent.common.platform_id
'''

import os, sys
if __name__ == '__main__':
    # FIXME, I'd really like a better way to do this- currently this is
    # hackish at best, and horrid at worst
    sys.path.insert(0, "%s/../" % os.path.dirname(__file__))
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

    def test_sysID(self):
        sysID = None
        try:
            stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --sysid')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                sysID = output[0]
        finally:
            stream.close()

        self.assertEqual(self.platformID.VARIANT.SYSID, sysID)

    def test_platform(self):
        platform = None
        try:
            stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --platform')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                platform = output[0]
        finally:
            stream.close()

        self.assertEqual(self.platformID.VARIANT.PLATFORM, platform)

    def test_isNotSingleton(self):
        dupID = PlatformID()

        self.assertNotEqual(dupID, self.platformID)

    def test_hasSameState(self):
        dupID = PlatformID()

        self.assertEqual(dupID.__dict__, self.platformID.__dict__)

if __name__ == '__main__':
    unittest.main()

# vim:set ai et sts=4 sw=4 tw=80:
