import sys, time
#sys.path.append('/Users/kramer/Downloads')

from flat_kivy_extensions.third_party.devslib.coverflowlayout import CoverFlowLayout

from kivy.metrics import dp
from kivy.uix.modalview import ModalView

class CoverFlowPopup(ModalView):

    def __init__(self, widgets, index_changed_callback=None, index=0, *largs, **kwargs):
        super(CoverFlowPopup, self).__init__(*largs, **kwargs)

        self.widgets = widgets

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


