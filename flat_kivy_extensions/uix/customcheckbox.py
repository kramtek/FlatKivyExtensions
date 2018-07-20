

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty

from flat_kivy.uix.flatcheckbox import FlatCheckBoxListItem, Check

from flat_kivy_extensions.uix.custombehaviors import CustomToggleButtonBehavior
from flat_kivy.uix.behaviors import (GrabBehavior, ThemeBehavior, TouchRippleBehavior,
                                     LogBehavior)


# Completely copy CheckBox -> _CheckBox
# Completely copy FlatCheckBox -> CustomCheckBox
#  - have CustomCheckBox use _CheckBox
#  - have _CheckBox inherit from CustomToggleButtonBehavior rather than ToggleButtonBehavior

class _CheckBox(CustomToggleButtonBehavior, Widget):
    '''CheckBox class, see module documentation for more information.
    '''

    active = BooleanProperty(False)
    '''Indicates if the switch is active or inactive.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.
    '''

    def __init__(self, **kwargs):
        self._previous_group = None
        super(_CheckBox, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if value == 'down':
            self.active = True
        else:
            self.active = False

    def _toggle_active(self):
        self._do_press()


class CustomCheckBox(GrabBehavior, TouchRippleBehavior,
                   LogBehavior, ThemeBehavior, _CheckBox):
    check = ObjectProperty(None)
    no_interact = BooleanProperty(False)
    check_scale = NumericProperty(.5)
    outline_size = NumericProperty(5)
    color_tuple = ListProperty(['Grey', '0000'])
    check_color_tuple = ListProperty(['Grey', '1000'])
    outline_color_tuple = ListProperty(['Grey', '1000'])
    ripple_color_tuple = ListProperty(['Grey', '1000'])

    radius = NumericProperty(5)
    size_scaling = NumericProperty(1)
    icon = StringProperty('fa-check')

    def __init__(self, **kwargs):
        super(CustomCheckBox, self).__init__(**kwargs)
        self.check = check = Check(scale=self.check_scale,
                                   color_tuple=self.check_color_tuple)
        self.bind(icon=self.check.setter('icon'))
        self.bind(pos=check.setter('pos'),
                  size=check.setter('size'),
                  check_scale=check.setter('scale'),
                  check_color_tuple=check.setter('color_tuple'))

    def on_active(self, instance, value):
        check = self.check
        if value and check not in self.children:
            self.add_widget(check)
        elif not value and check in self.children:
            self.remove_widget(check)

    def on_touch_down(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            super(CustomCheckBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            super(CustomCheckBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            super(CustomCheckBox, self).on_touch_up(touch)



class CustomSwitch(BoxLayout):
    no_interact = BooleanProperty(False)
    active = BooleanProperty(False)
    style = StringProperty('', allow_none=True)
    font_size = NumericProperty(10)

    def __init__(self, *largs, **kwargs):
        super(CustomSwitch, self).__init__(*largs, **kwargs)

    def on_touch_down(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            super(CustomSwitch, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            super(CustomSwitch, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            if self.collide_point(touch.x, touch.y):
                self.active = not self.active
            super(CustomSwitch, self).on_touch_up(touch)

    def on_active(self, instance, value):
        # print 'active value: %s' % str(value)
        if self.lbl1 in self.children:
            self.remove_widget(self.lbl1)
        if self.lbl2 in self.children:
            self.remove_widget(self.lbl2)
        if self.lbl3 in self.children:
            self.remove_widget(self.lbl3)

        if value:
            self.background_color = (.2,.5,.2, 1.0)
            self.add_widget(self.lbl1)
            self.add_widget(self.lbl2)
            self.switch_color = (.9, .9, .9, 1.0)
        else:
            self.background_color = (.9,.9,.9, 1.0)
            self.add_widget(self.lbl2)
            self.add_widget(self.lbl3)
            self.switch_color = (.5, .5, .5, 1.0)


class CustomSwitchListItem(BoxLayout, ThemeBehavior):
    flag = BooleanProperty(False)
    active = BooleanProperty(False)
    font_color_tuple = ListProperty(None, allow_none=True)
    style = StringProperty('', allow_none=True)
    switch_font_size = NumericProperty(10)

    def __init__(self, *largs, **kwargs):
        super(CustomSwitchListItem, self).__init__(*largs, **kwargs)

    #def on_active(self, instance, value):
    #    print 'im here...'


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

