


from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from flat_kivy.uix.behaviors import ThemeBehavior

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
        if self.collide_point(touch.x, touch.y):
            if not self.switch.collide_point(touch.x, touch.y):
                if not self.disabled:
                    self.switch.active = not self.switch.active
            else:
                return super(CustomSwitchListItem, self).on_touch_up(touch)
        super(CustomSwitchListItem, self).on_touch_up(touch)

    def on_disabled(self, instance, value):
        self.switch.disabled = value
        self.label.disabled = value




