__version__ = '0.0.1'

import logging, datetime
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class PackageLogger(object):

    def __init__(self, moduleName, moduleDebug=False):
        self.moduleName = moduleName
        self.moduleDebug = moduleDebug

    def _formattedNow(self):
        return datetime.datetime.now().strftime('%H:%M:%S.%f')[:-4]

    def debug(self, message):
        if self.moduleDebug:
            log.debug('%s: %s %s' % (self.moduleName, self._formattedNow(), message))

    def info(self, message):
        log.info('%s: %s %s' % (self.moduleName, self._formattedNow(), message))

    def warning(self, message):
        log.warning('%s: %s %s' % (self.moduleName, self._formattedNow(), message))

    def error(self, message):
        log.error('%s: %s %s' % (self.moduleName, self._formattedNow(), message))

