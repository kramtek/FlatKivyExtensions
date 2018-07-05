
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.properties import ListProperty, NumericProperty

from flat_kivy.uix.flatlabel import FlatLabel

from flat_kivy_extensions.uix.custombutton import CustomButton

from kivy.lang import Builder
Builder.load_string('''
<_MenuButton>:
    text_size: self.size
    halign: 'left'

''')

class _MenuButton(CustomButton):
    pass

class CustomDropDownButton(CustomButton):
    menubutton_theme = ListProperty([])
    menubutton_color = ListProperty((0,0,0,1))
    dropdown_width = NumericProperty(None, allownone=True)
    selected_item = NumericProperty(None, allownone=True)

    def __init__(self, items, *largs, **kwargs):
        super(CustomDropDownButton, self).__init__(*largs, **kwargs)
        self.dropdown = DropDown()
        self.buttons = list()
        self.items = items
        for text in items:
            #btn = _MenuButton(text=text, size_hint_y=None, height=dp(35))
            btn = _MenuButton(size_hint_y=None, height=dp(35))
            label = FlatLabel(text=text)
            label.style = btn.style
            label.text_size = btn.size
            label.halign = 'left'
            btn.add_widget(label)
            btn.label = label
            btn.radius = 0
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.label.text))
            self.dropdown.add_widget(btn)
            self.buttons.append(btn)
        self.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.on_select)

        self.text_size = self.size
        self.halign = 'left'
        self.valign = 'center'

    def on_menubutton_theme(self, instance, value):
        for btn in self.buttons:
            btn.theme = value
            btn.children[0].style = btn.style
            btn.radius = 0

    def on_menubutton_color(self, instance, value):
        for btn in self.buttons:
            btn.color = value

    def on_dropdown_width(self, instance, value):
        self.dropdown.auto_width = False
        #self.dropdown.size_hint_x = None
        self.dropdown.width = value

    def on_select(self, instance, value):
        self.text = value
        self.selected_item = self.items.index(value)

