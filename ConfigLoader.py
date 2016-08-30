# -*- coding: UTF-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import ConfigParser
import logging
from logging.config import fileConfig
import os,sys

#
# configuration file parsing
#
class ConfigLoader():
    # config parser instance
    cfgparser = None
    # config file name
    cfgfilename = None

    # configs' dict. key is section in cfg file!
    # e.g. config['mystuff']= ...
    config={}

    def __init__(self, cfgfilename, logger=None):

        if logger is None:
            # configures a simple console logger.
            logging.basicConfig()
            self.logger=logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate=False
            logFormatter = logging.Formatter("%(asctime)s %(process)s %(module)s %(levelname)s [-] %(message)s")
            consoleHandler=logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            self.logger.addHandler(consoleHandler)
        else:
            self.logger=logger

        self.logger.debug('init')

        self.cfgparser = ConfigParser.RawConfigParser()
        self.cfgfilename = cfgfilename

        if not os.path.isfile(cfgfilename):
            self.logger.critical('configuration file ' + cfgfilename + ' not found or not a file. giving up.')
            sys.exit(1)

        try:
            self.cfgparser.read(cfgfilename)
        except ConfigParser.ParsingError:
            self.logger.critical('parsing configuration file. giving up.')
            sys.exit(1)

    def parse_section(self, section, settings=None):

        if section is None or not self.cfgparser.has_section(section):
            return False

        # create the section dict in config
        self.config[section]={}

        # parse only provided settings' list, if any fails, returns immediately
        if settings is not None:
            ok=True
            # get these specific settings, others are silently ignored
            for setting in settings:
                if self.cfgparser.has_option(section, setting):
                    self.config[section][setting]=self.cfgparser.get(section, setting)
                    self.logger.debug('setting %s loaded from %s section', setting, section)
                else:
                    self.logger.warning('missing %s setting in %s configuration section', setting, section)
                    ok=False

            if not ok:
                return False

        # if settings is None, parse every setting
        else:
            for setting in self.cfgparser.options(section):
                self.config[section][setting]=self.cfgparser.get(section, setting)
                self.logger.debug('setting %s loaded from %s section', setting, section)

        return True

    def get_section(self, section):
        if section in self.config:
            return self.config[section]

    def get_sections(self):
        return self.config.keys()

    def get_section_setting(self, section, setting):
        if section in self.config:
            if setting in self.config[section]:
                return self.config[section][setting]
        self.logger.error('%s setting not found in %s config', setting, section)
        return None



if __name__ == '__main__':

    from pprint import pprint

    # config logging
    fileConfig('logging.cfg')
    logger=logging.getLogger(__name__)
    # end config logging.


    logger.info('testing %s', __name__)
    
    cfg=ConfigLoader('app.cfg', logger=logger)
    cfg.parse_section('mystuff')

    pprint(cfg.get_section('mystuff'))

