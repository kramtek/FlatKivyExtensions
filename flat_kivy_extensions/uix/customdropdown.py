
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

<_ColoredLabel>:
    canvas_color: (.8, 0.9, .8, 0.0)
    text_size: self.size
    halign: 'left'
    valign: 'middle'

    canvas.before:
        Color:
            rgba: root.canvas_color
        Rectangle:
            size: self.size
            pos: self.pos

''')

class _MenuButton(CustomButton):
    pass

class _ColoredLabel(FlatLabel):
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
            label = _ColoredLabel(text=text)
            label.style = btn.style
            #label.text_size = [btn.width*0.8, btn.height]
            label.text_size = btn.size
            btn.padding = dp(10)
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
        self.dropdown.width = value
        for btn in self.buttons:
            btn.size_hint_x = None
            btn.width = value
            btn.label.size_hint_x = None
            btn.label.width = value*0.8

    def on_select(self, instance, value):
        self.text = value
        self.selected_item = self.items.index(value)

