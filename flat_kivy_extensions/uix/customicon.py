
from os.path import join, dirname

from kivy.garden.iconfonts import register
from kivy.garden.iconfonts import icon as icon__

from kivy.properties import ListProperty, StringProperty

from flat_kivy.uix.flatlabel import FlatLabel

fn = join(dirname(__file__),'../data/font/')

register('test_font', fn + 'fa-solid-900.ttf', fn + 'fontawesome.fontd')

from flat_kivy.uix.flatlabel import FlatLabel
import flat_kivy
nfn = join(dirname(flat_kivy.__file__), 'data/font/')
register('orig_font', nfn + 'fontawesome-webfont.ttf', fn + 'fontawesome_old.fontd')

class CustomIcon(FlatLabel):
    color_tuple = ListProperty(['Grey', '600'])
    icon = StringProperty('')
    icon_family = StringProperty('test_font')


    #def on_color_tuple(self, instance, value):
    #    print('setting color tuple to: %s' % str(value))

    def on_icon(self, instance, value):
        try:
            self.text = "%s"%(icon__(self.icon, size=None, color=None, font_name='test_font')) if self.icon != '' else ''
        except:
            try:
                self.text = "%s"%(icon__(self.icon, size=None, color=None, font_name='orig_font')) if self.icon != '' else ''
            except:
                print('cannot find %s in any icon font...' % str(self.icon))
                return '?'

    #    print('setting icon for %s to: %s' % (str(self), str(value)))
    #    self.text = 'shit'
    #    self.color = (0,0,0,1)
    #    self.font_size = '25dp'
    #    self.size_hint = (None, None)
    #    self.size = ('20dp', '20dp')





