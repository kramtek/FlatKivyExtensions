

from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from flat_kivy.uix.behaviors import ThemeBehavior
from kivy.properties import NumericProperty, BoundedNumericProperty, BooleanProperty

from flat_kivy_extensions import PackageLogger
log = PackageLogger(__name__, moduleDebug=False)

class CustomPopupContent(GridLayout, ThemeBehavior):
    message = StringProperty('Default Popup Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )
    messge_alignment = StringProperty('center')

    icon = StringProperty('fa-check', allownone=True)
    spinner_color = ListProperty( [0.0, 0.6, 0.2, 0.8] )

    def __init__(self, *largs, **kwargs):
        super(CustomPopupContent, self).__init__(*largs, **kwargs)
        self._show_spinner = True

    def remove_ok_btn(self):
        self.btn_layout.remove_widget(self.ok_btn_layout)

    def remove_cancel_btn(self):
        self.btn_layout.remove_widget(self.cancel_btn_layout)

    def on_parent(self, instance, value):
        if self._show_spinner:
            self.spinner.start_spinning()

    def stop_spinning(self, instance):
        self.spinner.stop_spinning()

    def remove_spinner(self):
        self.spinner.stop_spinning()
        self.remove_widget(self.spinner)
        self._show_spinner = False

    def remove_icon(self):
        self.remove_widget(self.popup_icon)

    def setup_btn_layout(self, ok_text, cancel_text):
        pass


class CustomBusyContent(GridLayout, ThemeBehavior):
    message = StringProperty('Default Busy Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )

    def __init__(self, cancel_callback=None, **kwargs):
        super(CustomBusyContent, self).__init__(**kwargs)
        self.cols = 1

class CustomErrorContent(GridLayout, ThemeBehavior):
    message = StringProperty('Default error Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )

    def __init__(self, cancel_callback=None, **kwargs):
        super(CustomErrorContent, self).__init__(**kwargs)
        self.cols = 1


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
        log.debug('updating spinner...')
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


