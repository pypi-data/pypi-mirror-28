from abc import ABCMeta, abstractmethod

import os

from pf_manager.util.log import logger


class BaseCommand(object):
    def __init__(self, config):
        self.config = config
        self.config_path = config.obj["config"]
        if not os.path.exists(self.config_path):
            logger.info('Creating setting file of pfm in ' + self.config_path + '...')
            f = open(self.config_path, 'w')
            f.write('{}')
            f.close()

    @abstractmethod
    def run(self):
        pass
