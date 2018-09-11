


from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customiconbutton import CustomIconButton

from flat_kivy.fa_icon_definitions import fa_icons
fontd = {}

from os.path import join, dirname
import json

import flat_kivy_extensions
fn = dirname(flat_kivy_extensions.__file__) + '/data/font/fontawesome.fontd'
with open(fn, 'r') as f:
    fontd = json.loads(f.read())

#fontd = fa_icons

Builder.load_string('''
<-IconDemoScreen>:
    title: 'Icon Demo Screen'
    theme: ('app', 'screen')

''')

class IconDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(IconDemoScreen, self).__init__(*largs, **kwargs)

        layout = StackLayout(orientation='lr-tb')

        l = sorted(fontd.keys())
        for icon in l:
            print('icon: %s' % str(icon))
            btn = CustomIconButton(text=icon, icon=icon)
            btn.theme = ('app', 'tabbarbutton')
            btn.size_hint = (None, None)
            btn.size = (dp(60), dp(75))
            btn.icon_font_size = '16dp'
            layout.add_widget(btn)

        #for index in xrange(10):
        #    btn = CustomIconButton(text=' ', icon='')
        #    btn.theme = ('app', 'tabbarbutton')
        #    btn.size_hint = (None, None)
        #    btn.size = (dp(60), dp(75))
        #    layout.add_widget(btn)

        l2 = sorted(fa_icons.keys())
        for icon in l2:
            if icon in l:
                print('found duplicate: %s' % str(icon))
                continue
            print('icon: %s' % str(icon))
            btn = CustomIconButton(text=icon, icon=icon)
            btn.theme = ('app', 'tabbarbutton')
            btn.size_hint = (None, None)
            btn.size = (dp(60), dp(75))
            btn.icon_font_size = '16dp'
            btn.font_color_tuple = ('Blue', '500')
            layout.add_widget(btn)

        self.add_widget(layout)

        layout.size_hint_y = None
        layout.height = dp(10000)




