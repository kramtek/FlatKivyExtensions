

import sys, time
#sys.path.append('/Users/kramer/Downloads')

from devslib.coverflowlayout import CoverFlowLayout
from devslib.coverflow import _CoreImage

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.modalview import ModalView

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<-NavigationScreen>:
    canvas.before:
        Color:
            rgba: (0.05, 0.1, 0.05, 1.0)
        Rectangle:
            size: self.size
            pos: self.pos


<CoverFlowPopup>:

''')

class CoverFlowPopup(ModalView):

    def __init__(self, widgets, index_changed_callback=None, index=0, *largs, **kwargs):
        super(CoverFlowPopup, self).__init__(*largs, **kwargs)

        self.widgets = widgets

        print 'should set index to: %s' % str(index)
        self.index_changed_callback = index_changed_callback
        lst_covers = widgets
        cover_names = list()
        for widget in widgets:
            cover_names.append(str(id(widget)))
        self.cfl = CoverFlowLayout(lst_covers, cover_names, cover_change_callback=self._cover_changed, index=index)
        self.cfl.size_hint = (None,None)
        self.cfl.size = (dp(0), dp(0))
        self.add_widget(self.cfl)
        self.auto_dismiss = False

        self.size_hint = (None, None)
        self.size = (1,1)

    def _cover_changed(self, index):
        self.index_changed_callback(index)
        self.dismiss()
        return
        # sm = App.get_running_app()._screenmanager
        # screen = sm.screens[index]
        # print 'coverflow navigation switch to screen: %s' % str(screen.name)
        # sm.current = screen.name
        # self.dismiss()

class NavigationScreen(Screen):

    def __init__(self, thumbnails, *largs, **kwargs):
        super(NavigationScreen, self).__init__(*largs, **kwargs)

        _lst_covers = [
          '/Users/kramer/mobilabui/data/images/python.png',
          '/Users/kramer/mobilabui/data/images/icube_0.png',
          '/Users/kramer/mobilabui/data/images/copain_0.png',
          '/Users/kramer/mobilabui/data/images/hi_left_blue.png',
          '/Users/kramer/mobilabui/data/images/python.png',
          '/Users/kramer/mobilabui/data/images/hi_left_blue.png',
          '/Users/kramer/mobilabui/data/images/python.png',
          '/Users/kramer/mobilabui/data/images/hi_left_blue.png',
          '/Users/kramer/mobilabui/data/images/python.png',
        ]
        self.lst_covers = []
        self.cover_names = _lst_covers

        for name in _lst_covers:
            #self.lst_covers.append(_CoreImage(name).texture)
            self.lst_covers.append(name)

        (self.lst_covers, self.cover_names) = zip(*thumbnails)
        self.add_widget(CoverFlowLayout(self.lst_covers, self.cover_names, cover_change_callback=self._cover_changed))

    def _cover_changed(self, index):
        sm = self.parent
        screen = sm.screens[index]
        print 'coverflow navigation switch to screen: %s' % str(screen.name)
        sm.current = screen.name

    def do_layout(self, *largs):
        print 'do layout...'
        super(NavigationScreen, self).do_layout(*largs)

    def on_enter(self, *largs):
        print 'entered navigation screeen.'
        cfl = self.children[0]
        print '  cfl coverflow image size: %s' % str(cfl.coverflow.covers[0].image.size)
        print '  cfl coverflow cover size: %s' % str(cfl.coverflow.covers[0].size)
        time.sleep(2.0)
        print '  cfl coverflow image size: %s' % str(cfl.coverflow.covers[0].image.size)
        print '  cfl coverflow cover size: %s' % str(cfl.coverflow.covers[0].size)

        print 'cover scales: '
        for cover in cfl.coverflow.covers:
            print '    cover scale_y: %s' % str(cover.scale_y)

    def on_size(self, instance, value):
        print 'on_size for screen...'

    def on_pre_enter(self, *largs):
        print 'about to enter: %s' % str(largs)
        cfl = self.children[0]
        print '  cfl coverflow image size: %s' % str(cfl.coverflow.covers[0].image.size)
#        for cover in cfl.coverflow.covers:
#            print '    cover size: %s' % str(cover.image.size)

