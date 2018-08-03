

from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from flat_kivy.uix.behaviors import ThemeBehavior
from kivy.properties import NumericProperty, BoundedNumericProperty, BooleanProperty

class CustomPopupContent(GridLayout, ThemeBehavior):
    text = StringProperty('Default Error Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )
    messge_alignment = StringProperty('center')

class CustomBusyContent(GridLayout, ThemeBehavior):
    busy_text = StringProperty('Default Busy Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )

    def __init__(self, cancel_callback=None, **kwargs):
        super(CustomBusyContent, self).__init__(**kwargs)


class CustomSpinner(Widget):
    color = ListProperty([.1, 1, 1, 1])
    speed = BoundedNumericProperty(1, min=0.1)
    advance_speed = NumericProperty(0)
    stroke_length = BoundedNumericProperty(25., min=1, max=180)
    stroke_width = NumericProperty(None, allownone=True)

    _angle_center = NumericProperty(0)
    _angle_start = NumericProperty(0)
    _angle_end = NumericProperty(1)
    _size = NumericProperty()
    _rsize = NumericProperty()
    _stroke = NumericProperty(1)
    _radius = NumericProperty(50)

    _opening_state = BooleanProperty(True)

    def start_spinning(self, *largs):
        Clock.schedule_interval(self._update, .1)

    def stop_spinning(self, *args):
        Clock.unschedule(self._update)

    def _update(self, dt):
        angle_speed = 90. * self.speed
        angle_advance_speed = 90. * self.advance_speed
        self._angle_center += 1.0*(dt * angle_advance_speed)

        if self._opening_state:
            self._angle_end = (self._angle_end + dt * angle_speed)
            if self._angle_end >= 360:
                self._angle_end = 359
                self._angle_start = 0
                self._opening_state = False
        else:
            self._angle_start = (self._angle_start + dt * angle_speed)
            if self._angle_start >= 360:
                self._angle_end = 0
                self._angle_start = 0
                self._opening_state = True


