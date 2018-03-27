

from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty

from flat_kivy.uix.flatcheckbox import FlatCheckBox, FlatCheckBoxListItem, Check

from flat_kivy.uix.behaviors import ToggleButtonBehavior


class CustomCheckBox(FlatCheckBox):
    radius = NumericProperty(20)
    size_scaling = NumericProperty(1)
    icon = StringProperty('fa-check')
    radius = NumericProperty(5)

    def __init__(self, **kwargs):
        super(CustomCheckBox, self).__init__(**kwargs)
        self.bind(icon=self.check.setter('icon'))


class CustomCheckBoxListItem(FlatCheckBoxListItem):
    icon = StringProperty('fa-check')
    size_scaling = NumericProperty(1)
    radius = NumericProperty(50)
    active = BooleanProperty(False)
    current_state = BooleanProperty(False)
    check_color_tuple_down = ListProperty(None, allow_none=True)
    check_color_hue_down = StringProperty(None, allow_none=True)

    exclusive = BooleanProperty(True)

    def __init__(self, *largs, **kwargs):
        self.checkbox_active = BooleanProperty(False)
        self.up_color_tuple = ('Gray', '500')

        super(CustomCheckBoxListItem, self).__init__(*largs, **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.up_color_tuple = self.check_color_tuple
            if self.check_color_tuple_down is not None:
                if len(self.check_color_tuple_down) > 0:
                    self.check_color_tuple = self.check_color_tuple_down
            if self.check_color_hue_down is not None:
                self.check_color_tuple = (self.check_color_tuple[0], self.check_color_hue_down)
            self.toggle_checkbox()
        super(FlatCheckBoxListItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.active = self.checkbox_active
            self.check_color_tuple = self.up_color_tuple
            super(FlatCheckBoxListItem, self).on_touch_up(touch)

    def on_checkbox_active(self, instance, active):
        self.checkbox_active = active

    def on_current_state(self, instance, state):
        if self.active is not state:
            self.toggle_checkbox()

