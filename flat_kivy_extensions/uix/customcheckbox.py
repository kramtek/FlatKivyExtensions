

from kivy.metrics import dp
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
    disabled = BooleanProperty(False)

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
#        print('on active...: %s' % str(value))
        if value and check not in self.children:
#            print('adding widget...')
            self.add_widget(check)
        elif not value and check in self.children:
#            print('removing widget...')
            self.remove_widget(check)

    def on_touch_down(self, touch):
#        print('checkbox on touch down...')
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            return super(CustomCheckBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            return super(CustomCheckBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
#        print('check box on touch up...')
        if self.no_interact:
            if self.collide_point(touch.x, touch.y):
                return False
        else:
            #if self.collide_point(touch.x, touch.y):
            #    print('toggling active... was: %s' % str(self.active))
            #    #self.active = not self.active
            #    #self.checkbox.toggle_checkbox()
            #    print('   now: %s' % str(self.active))
            return super(CustomCheckBox, self).on_touch_up(touch)

    def on_no_interact(self, instance, value):
#        print('setting check no interact to: %s' % str(value))
        self.check.no_interact = value


class CustomSwitch(BoxLayout):
    no_interact = BooleanProperty(False)
    active = BooleanProperty(False)
    style = StringProperty(None, allow_none=True)
    font_size = NumericProperty(10)
    disabled = BooleanProperty(False)

    switch_color_active =            (.3, .6, .3, 1.0)
    switch_color_inactive =          (.5, .5, .5, 1.0)
    switch_color_active_disabled =   (.6, .7, .6, 1.0)
    switch_color_inactive_disabled = (.8, .8, .8, 1.0)

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
                if not self.disabled:
                    self.active = not self.active
                else:
                    if self.active:
                        self.switch_color = self.switch_color_active_disabled
                    else:
                        self.switch_color = self.switch_color_inactive_disabled
                    return False
            super(CustomSwitch, self).on_touch_up(touch)

    def on_disabled(self, instance, disabled):
        if disabled:
            if self.active:
                self.switch_color = self.switch_color_active_disabled
            else:
                self.switch_color = self.switch_color_inactive_disabled
        else:
            if self.active:
                self.switch_color = self.switch_color_active
            else:
                self.switch_color = self.switch_color_inactive

    def on_active(self, instance, value):
        if self.lbl1 in self.children:
            self.remove_widget(self.lbl1)
        if self.lbl2 in self.children:
            self.remove_widget(self.lbl2)
        if self.lbl3 in self.children:
            self.remove_widget(self.lbl3)

        if value:
            #self.background_color = (.2,.5,.2, 1.0)
            self.add_widget(self.lbl1)
            self.add_widget(self.lbl2)
            self.switch_color = self.switch_color_active
        else:
            #self.background_color = (.9,.9,.9, 1.0)
            self.add_widget(self.lbl2)
            self.add_widget(self.lbl3)
            self.switch_color = self.switch_color_inactive


class CustomSwitchListItem(BoxLayout, ThemeBehavior):
    flag = BooleanProperty(False)
    active = BooleanProperty(False)
    font_color_tuple = ListProperty(None, allownone=True)
    style = StringProperty(None, allownone=True)
    font_size = NumericProperty( 15 )
    switch_font_size = NumericProperty(10)
#    disabled = BooleanProperty(False)

    def __init__(self, *largs, **kwargs):
        super(CustomSwitchListItem, self).__init__(*largs, **kwargs)

    def on_active(self, instance, value):
        self.switch.active = value

    def on_touch_up(self, touch):
        #return super(CustomSwitchListItem, self).on_touch_up(touch)

        if self.collide_point(touch.x, touch.y):
            if not self.switch.collide_point(touch.x, touch.y):
                if not self.disabled:
#                    print('should toggle switch...')
                    self.switch.active = not self.switch.active
            else:
                return super(CustomSwitchListItem, self).on_touch_up(touch)
        super(CustomSwitchListItem, self).on_touch_up(touch)

    def on_disabled(self, instance, value):
        self.switch.disabled = value
        self.label.disabled = value



class CustomCheckBoxListItem(FlatCheckBoxListItem):
    icon = StringProperty('fa-check')
    size_scaling = NumericProperty(1)
    radius = NumericProperty(50)
    active = BooleanProperty(False)
    current_state = BooleanProperty(False)
#    check_color_tuple_down = ListProperty(None, allow_none=True)
#    check_color_hue_down = StringProperty(None, allow_none=True)

    exclusive = BooleanProperty(True)
    disabled = BooleanProperty(False)
    font_size = NumericProperty( dp(15) )
    detail_text = StringProperty('', allow_none=True )
    detail_font_size = NumericProperty(dp(1))
    no_interact = BooleanProperty(False)

    def __init__(self, *largs, **kwargs):
        self.checkbox_active = BooleanProperty(False)
        self.up_color_tuple = ('Gray', '500')

        super(CustomCheckBoxListItem, self).__init__(*largs, **kwargs)

#    def on_no_interact(self, instance, value):
#        print('setting checkbox no interact to: %s' % str(value))
#        self.checkbox.no_interact = value

    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return False
        if (self.disabled or self.no_interact):
#            print('disabled: %s' % str(self.disabled))
#            print('no_interact: %s' % str(self.no_interact))
            return False
        return super(CustomCheckBoxListItem, self).on_touch_down(touch)

    def on_disabled(self, instance, value):
#        print('largs: %s' % str((instance, value)))
#        if not value:
#            self.no_interact = value
#        else:
#            self.no_interact = value
        return super(CustomCheckBoxListItem, self).on_disabled(instance, value)
#        return super(CustomCheckBoxListItem, self).on_disabled(*largs)
#        print('on disabled: %s' % str(value))

#        self.no_interact = value

#        if self.collide_point(touch.x, touch.y):
#            self.up_color_tuple = self.check_color_tuple
#            if self.check_color_tuple_down is not None:
#                if len(self.check_color_tuple_down) > 0:
#                    self.check_color_tuple = self.check_color_tuple_down
#            if self.check_color_hue_down is not None:
#                self.check_color_tuple = (self.check_color_tuple[0], self.check_color_hue_down)
#            self.toggle_checkbox()
#        super(CustomCheckBoxListItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        #self.checkbox.check_color_tuple = self.check_color_tuple
#        print('check color tuple: %s' % str(self.checkbox.check.color_tuple))
        return super(CustomCheckBoxListItem, self).on_touch_up(touch)


    def _on_touch_up(self, touch):
        if self.checkbox.collide_point(touch.x, touch.y):
            return False
        return super(CustomCheckBoxListItem, self).on_touch_up(touch)
#        if self.disabled:
#            if self.collide_point(touch.x, touch.y):
#                return False
#        if self.collide_point(touch.x, touch.y):
#            print('\n\ncollided point in check box list item: %s' % str(self))
#            self.active = self.checkbox_active
#            if not self.checkbox.collide_point(touch.x, touch.y):
#                print('  not in actual checkbox...')
#                #self.checkbox.active = not self.checkbox.active
#                return False
#            else:
#                print(' in actual checkbox...')
#                #self.toggle_checkbox()
#                return super(CustomCheckBoxListItem, self).on_touch_up(touch)
#            self.check_color_tuple = self.up_color_tuple
#            super(CustomCheckBoxListItem, self).on_touch_up(touch)


    #def on_checkbox_active(self, instance, active):
    #    return
    #    self.checkbox_active = active

    def on_current_state(self, instance, state):
        if self.active is not state:
            self.toggle_checkbox()

