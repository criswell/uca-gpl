import sys, os

sys.path.insert(0, os.path.dirname(__file__))

ALL_TESTS =
    [
        'test_platform_id.py',
    ]

for test in ALL_TESTS:
    # FIXME - surely there's a better way to do this
    line = "python tests/%s" % test
    print os.system(line)

# vim:set ai et sts=4 sw=4 tw=80:
