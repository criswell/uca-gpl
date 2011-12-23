import os
import ConfigParser as configparser

def setup_conf(conf_file):
    config = configparser.RawConfigParser()
    if os.path.isfile(conf_file):
        config.read(conf_file)
    else:
        # No file exists, make a sensible default
        config.add_section('main')
        config.set('main', 'log_level', '4')
        config.set('main', 'sleep_timer', '30')
        config.set('main', 'registration_attempts', '10')
        config.set('main', 'poll_retry_attempts', '20')

        # FIXME - Stupid RHEL, its ancient python is preventing us from using
        # 'with', so we need to wrap this in an old-school try-finally, but I
        # forget the exceptions that open can toss at the moment, so I'm
        # putting in this FIXME

        # Writing our configuration file to 'example.cfg'
        configfile = open(conf_file, 'wb')
        config.write(configfile)
        configfile.close()

    return config

# vim:set ai et sts=4 sw=4 tw=80:
