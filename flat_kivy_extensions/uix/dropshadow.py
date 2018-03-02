

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

Builder.load_string('''
#: import ew kivy.uix.effectwidget

<-DropShadow>:
    blur_rad: 8.0
    offset: 5
    background_color: (1.0, 1.0, 1.0, 1.0)
    shadow_color: (0.1, 0.1, 0.1, 0.6)

    radius: 0

    size_hint: None, None
    size: dp(10), dp(15)
    widget_size: dp(10), dp(10)
    container_size: dp(15), dp(15)
    overhead: dp(15)

    anchor_x: 'left'
    anchor_y: 'top'

    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        size: root.container_size

        canvas.before:
            Color:
                rgba: (.1, .2, .3, 1)
            Rectangle:
                size: self.size
                pos: self.pos

        EffectWidget:

            blur_rad: root.blur_rad

            effects: ew.VerticalBlurEffect(size=dp(self.blur_rad)), ew.HorizontalBlurEffect(size=dp(self.blur_rad))
            background_color: root.background_color
            size_hint: None, None
            size: root.container_size

            canvas.before:
                Color:
                    rgba: (.1, .2, .3, 1.0)
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                size_hint: None, None
                size: root.widget_size
                offset_x: root.offset
                offset_y: root.overhead-root.offset

                canvas.before:
                    Color:
                        rgba: root.shadow_color
                    RoundedRectangle:
                        size: self.size
                        pos: (self.pos[0] + dp(self.offset_x), self.pos[1] + dp(self.offset_y))
                        radius: [dp(root.radius),dp(root.radius),dp(root.radius),dp(root.radius)]

                on_parent: root._add_widget_to_shadow()
''')


class DropShadow(AnchorLayout):
    def __init__(self, widget, *largs, **kwargs):
        self.widget = widget
        super(DropShadow, self).__init__(*largs, **kwargs)

    def _add_widget_to_shadow(self):
        self.widget.bind(size=self._resize)
        self._resize(self.widget, None)
        self.add_widget(self.widget)

    def _resize(self, instance, value):
        self.size = (instance.width, instance.height+dp(15))
        overhead = 22
        self.container_size = (instance.width + dp(overhead), instance.height + dp(overhead))
        self.overhead = overhead
        self.widget_size = instance.size


