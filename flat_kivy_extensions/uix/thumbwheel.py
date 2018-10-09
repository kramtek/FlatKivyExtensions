
import math

from kivy.lang import Builder

from kivy.clock import Clock, mainthread
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty

from flat_kivy.uix.flatlabel import FlatLabel

from flat_kivy_extensions import AppAwareThread

from flat_kivy_extensions import PackageLogger
log = PackageLogger(__name__, moduleDebug=True)

_debug_layout = False

Builder.load_string('''

<-ExtendedThumbWheel>:
    cols: 1
    padding: [dp(1), dp(1), dp(1), dp(5)]
    # canvas.before:
    #     Color:
    #         rgba: (0.4, 0.5, 0.4, 0.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos


<_TitleLabel>:
    text_size: self.size
    halign: 'center'
    size_hint_y: None
    # canvas.before:
    #     Color:
    #         rgba: (0.8, 0.4, 0.4, 0.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

<_ColoredLabel>:
    text_size: self.size
    halign: 'center'
    size_hint_y: None
    canvas.before:
        Color:
            rgba: (0.8, 0.4, 0.4, 0.3)
        Rectangle:
            size: self.size
            pos: self.pos

<_ColoredGridLayout>:
    color: (.2, 0.9, .2, 0.0)
    canvas.before:
        Color:
            rgba: root.color
        Rectangle:
            size: self.size
            pos: self.pos

<_ColoredThumbWheelLabel>:
    size_hint_y: None
    text_size: self.size
    halign: 'center'
    canvas.before:
        Color:
            rgba: root.canvas_color
        Rectangle:
            size: [self.size[0], self.size[1]*0.95]
            pos: self.pos

<_ThumbWheelWidget>:
    orientation: 'vertical'
    # canvas.before:
    #     Color:
    #         rgba: (0.0, 0.0, 0.2, 0.3)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

''')

class _ColoredThumbWheelLabel(FlatLabel):
    scaled_index = NumericProperty(None, allownone=True)
    phase = NumericProperty(None, allownone=True)
    height_scaling = NumericProperty(0)

    color_max = ListProperty([.5, .8, .6, 1.0])
    color_min = ListProperty([.01, .01, .01, 1.0])

    canvas_color = ListProperty( [.01, .01, .01, .5])

    def __init__(self, **kwargs):
        self._height_scaling = 1.0
        self._canvas_color = [0]*4
        super(_ColoredThumbWheelLabel, self).__init__(**kwargs)
        self.bind(color_max=self.configure)
        self.bind(color_min=self.configure)

    def on_height_scaling(self, instance, value):
        self._height_scaling = float(value)

    def configure(self, instance, value):
        self.on_phase(self, self.phase)

    def on_phase(self, instance, phase):
        sine_value = math.sin(self.scaled_index * 2*math.pi + phase)
        self.height = max(sine_value,0) * float(self._height_scaling)

        # if sine_value < 0:
        #     return

        j = sine_value

        for index, (color_max, color_min) in enumerate(zip(self.color_max, self.color_min)):
            self._canvas_color[index] = color_max*abs(j) + color_min*(1-abs(j))
        self.canvas_color = self._canvas_color


class _ColoredGridLayout(GridLayout):
    pass


class _ColoredLabel(FlatLabel):
    pass


class _TitleLabel(FlatLabel):
    pass


class ExtendedThumbWheel(GridLayout):
    label_text = StringProperty('Label')
    label_format = StringProperty('%2.3f')
    units = StringProperty('')

    value_max = NumericProperty(1.0)
    value_min = NumericProperty(0.0)
    color_max = ListProperty([.5, .8, .6, 1.0])
    color_min = ListProperty([.01, .01, .01, 1.0])

    scroll_height_ratio = NumericProperty(4.0)
    rotation_scale = NumericProperty(1.0)

    spinner_width = NumericProperty(dp(40))

    disabled = BooleanProperty(False)

    def __init__(self, while_spinning_callback=None, **kwargs):
        self._is_spinning = False
        self._continue_spinning = False
        self._value = None
        self._event = None
        self._while_spinning_callback = while_spinning_callback
        self._last_position = None

        super(ExtendedThumbWheel, self).__init__(**kwargs)

        self.spacing = dp(3)
        self.label = _TitleLabel(text='', color_tuple=('Brown', '700'), height=dp(40),)
        self.label.style = 'NavigationLabelSubHeading'

        thumbwheel_container = BoxLayout( size_hint=(None, None),
                                       size=(self.width, self.height-self.label.height - self.padding[3]), )

        self.thumbwheel = ThumbWheel( size_hint=(None, None),
                                      size=(self.width-dp(20), self.height-self.label.height - self.spacing[1] - self.padding[3]), )

        self.thumbwheel.set_value(self.thumbwheel.value_min)

        self.bind(value_min=self.thumbwheel.setter('value_min'))
        self.bind(value_max=self.thumbwheel.setter('value_max'))
        self.bind(color_max=self.thumbwheel.setter('color_max'))
        self.bind(color_min=self.thumbwheel.setter('color_min'))

        self.thumbwheel.color_max = self.color_max
        self.thumbwheel.color_min = self.color_min

        self.bind(scroll_height_ratio=self.thumbwheel.setter('scroll_height_ratio'))
        self.bind(rotation_scale=self.thumbwheel.setter('rotation_scale'))

        thumbwheel_container.add_widget(Widget())
        thumbwheel_container.add_widget(self.thumbwheel)
        thumbwheel_container.add_widget(Widget())

        self.add_widget(self.label)
        self.add_widget(thumbwheel_container)

        self.thumbwheel.bind(value=self.update_value)

    def on_disabled(self, instance, value):
        if value:
            self.thumbwheel.scrollview.do_scroll_y = False
            self.thumbwheel.color_max = [.8, .8, .8, 1.0]
            self.thumbwheel.color_min = [.2, .2, .2, 1.0]
        else:
            self.thumbwheel.scrollview.do_scroll_y = True
            self.thumbwheel.color_max = self.color_max
            self.thumbwheel.color_min = self.color_min

    def update_value(self, instance, value):
        log.debug('updating value to: %s' % str(value))
        a = self.label_format % value
        self.label.text = self.label_text + ':\n' + a + ' ' + self.units

        self._value = value

        if self._while_spinning_callback is None:
            return

        if not self._is_spinning:
            self._is_spinning = True
            self._continue_spinning = True
            log.debug('  spawning thread...')
            AppAwareThread(target=self._threaded_process, show_busy=True).start()

        if self._event is not None:
            self._event.cancel()
        self._event = Clock.create_trigger(self._stop_process, 0.20)
        self._event()

    def _threaded_process(self):
        log.debug('  starting thread...')
        if self._while_spinning_callback is None:
            self._is_spinning = False
            return
        while self._continue_spinning:
            self._while_spinning_callback(self._value)
        self._is_spinning = False

    def _stop_process(self, *largs):
        self._continue_spinning = False
        self._event = None

    @mainthread
    def set_value(self, value):
        log.debug('Step 1: setting value for thumbwheel widget...')
        if self._is_spinning:
            log.debug('  but we cannot set the value if the wheel is spinning...')
            return
        self.thumbwheel.set_value(value)

    def on_spinner_width(self, instance, value):
        self.thumbwheel.thumbwheel_widget.width = value
        self.thumbwheel.thumbwheel_widget.center_x = self.thumbwheel.center_x


class _ThumbWheelWidget(BoxLayout):
    pass


class ThumbWheel(RelativeLayout):

    value = NumericProperty(None, allownone=True)
    value_max = NumericProperty(1.0)
    value_min = NumericProperty(0.0)
    color_max = ListProperty([.6, .8, .6, 1.0])
    color_min = ListProperty([.01, .01, .01, 1.0])

    scroll_height_ratio = NumericProperty(4.0)
    rotation_scale = NumericProperty(2.0)
    num_segments = NumericProperty(40)

    spinner_width = NumericProperty(dp(40))

    phase = NumericProperty(0)

    def __init__(self, *largs, **kwargs):
        self._last_position = None
        super(ThumbWheel, self).__init__(*largs, **kwargs)

        self.scrollview = ScrollView(size_hint=self.size_hint, size=self.size,
                                     bar_color=(.1,.3,.1,0.0),
                                     bar_inactive_color=(.3,.3,.1,0.0),
                                     )
        self.scrollview.effect_cls = ScrollEffect
        self.scrollview.scroll_distance = 0
        self.scrollview.scroll_timeout = 2000
        self._touch_copy = None

        self.gridlayout = _ColoredGridLayout(cols=1, size_hint=(None, None), size=(self.width, 0))
        self.gridlayout.bind(minimum_height=self.gridlayout.setter('height'))

        if not _debug_layout:
            self._scrolled_label = FlatLabel(text='', size_hint_y=None, height=self.height * self.scroll_height_ratio)
            self.gridlayout.add_widget(self._scrolled_label)

        else:
            self.numLabels = 100
            self._scrolled_labels = list()
            for index in xrange(self.numLabels):
                scrolled_label = _ColoredLabel(text='%s' % str(index), height=self.height * self.scroll_height_ratio / float(self.numLabels))
                self.gridlayout.add_widget(scrolled_label)
                scrolled_label.color = (0,0,0,1)
                scrolled_label.font_size = dp(8)
                self._scrolled_labels.append(scrolled_label)

        self.scrollview.add_widget(self.gridlayout)

        self.thumbwheel_widget = _ThumbWheelWidget(size_hint=self.size_hint, size=(self.spinner_width, self.height))
        self.ht_sum = 0
        self.labels = list()
        for i in range(self.num_segments):
            label = _ColoredThumbWheelLabel(text='', height=400/20.0,
                             color_tuple=('Brown', '700'), font_size=dp(8),
                             phase=0,
                             scaled_index=i/float(self.num_segments),
                             color_max=self.color_max, color_min=self.color_min)
            self.thumbwheel_widget.add_widget(label)
            self.labels.append(label)
            j = math.sin(i/float(self.num_segments) * 2*math.pi)
            ht = max(self.height/self.num_segments * j,0)
            self.ht_sum += ht

        for label in self.labels:
            label.height_scaling = self.height/self.num_segments * self.height/self.ht_sum

            self.bind(color_max=label.setter('color_max'))
            self.bind(color_min=label.setter('color_min'))
            self.bind(phase=label.setter('phase'))

        self.add_widget(self.scrollview)
        self.add_widget(self.thumbwheel_widget)

        self.thumbwheel_widget.center_x = self.scrollview.center_x
        self.scrollview.bind(scroll_y=self.on_scroll_y)
        self.on_scroll_y(self.scrollview, 1.0)

    def on_scroll_height_ratio(self, instance, value):
        if not _debug_layout:
            self._scrolled_label.height = self.height * value
            return
        for label in self._scrolled_labels:
            label.height = self.height*value / float(self.numLabels)

    def set_value(self, value):
        log.debug('  updating scroll y from external')
        self.scrollview.scroll_y = 1 - (value - self.value_min) / (self.value_max - self.value_min)

    def on_scroll_y(self, instance, scroll_position):
        if self._last_position is not None:
            if abs(self._last_position - scroll_position) < .00000001:
                return
        self._last_position = scroll_position
        log.debug('Scrolled to position: %0.15f' % scroll_position)
        phase = (scroll_position-1)*2*math.pi*self.rotation_scale % (-1*math.pi)
        log.debug('  mapped to phase: %s' % str(phase/math.pi * 180.0))
        self.phase = phase
        log.debug('got scroll so updating value...')
        self.value = (1-scroll_position)*(self.value_max - self.value_min) + self.value_min

    def on_color_max(self, instance, value):
        self.on_scroll_y(None, self.scrollview.scroll_y)

    def on_color_min(self, instance, value):
        self.on_scroll_y(None, self.scrollview.scroll_y)
