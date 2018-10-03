__version__ = '0.0.1'

import logging, datetime, threading, platform, sys, traceback
from kivy.app import App

log = logging.getLogger()
log.setLevel(logging.DEBUG)

if platform.machine().lower().startswith('iphone') or platform.machine().lower().startswith('ipod'):
    #log.handlers = []
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

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


class AppAwareThread(threading.Thread):

    def __init__(self, **kwargs):
        self._show_busy = kwargs.get('show_busy', False)
        if 'show_busy' in kwargs.keys():
            del kwargs['show_busy']
        super(AppAwareThread, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.daemon = True
        self._target = kwargs.get('target')

    def run(self):
        try:
            if self._show_busy:
                App.get_running_app().indicate_busy(True)
            super(AppAwareThread, self).run()
            if self._show_busy:
                App.get_running_app().indicate_busy(False)
        except Exception as e:
            tb = traceback.format_exc()
            targetString = str(self._target).strip().split(' ')[2]
            App.get_running_app().raise_error('Exception:', 'Exception in %s\n\n%s' % (targetString, str(e)),
                                          auto_dismiss=False, traceback=tb)
            if self._show_busy:
                App.get_running_app().indicate_busy(False)


