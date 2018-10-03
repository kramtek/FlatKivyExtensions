
import math

from kivy.lang import Builder

from kivy.clock import Clock
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

Builder.load_string('''

<-ExtendedThumbWheel>:
    cols: 1
    padding: [dp(1), dp(1), dp(1), dp(5)]
    canvas.before:
        Color:
            rgba: (0.4, 0.5, 0.4, 0.0)
        Rectangle:
            size: self.size
            pos: self.pos


<_ColoredGridLayout>:
    color: (.8, 0.9, .8, 0.0)
    canvas.before:
        Color:
            rgba: root.color
        Rectangle:
            size: [self.size[0], self.size[1]*0.95]
            pos: self.pos

<_ColoredThumbWheelLabel>:
    canvas_color: (.8, 0.9, .8, 0.0)
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
    canvas.before:
        Color:
            rgba: (0.0, 0.0, 0.0, 0.3)
        Rectangle:
            size: self.size
            pos: self.pos

''')

class _ColoredThumbWheelLabel(FlatLabel):
    pass


class _ColoredGridLayout(GridLayout):
    pass


class ExtendedThumbWheel(GridLayout):
    label_text = StringProperty('Label')
    label_format = StringProperty('%2.3f')
    units = StringProperty('')

    value = NumericProperty(None, allownone=True)
    value_max = NumericProperty(1.0)
    value_min = NumericProperty(0.0)
    #color = ListProperty([.3, .4, .3, 0.5])
    color_max = ListProperty([.5, .8, .6, 1.0])
    color_min = ListProperty([.01, .01, .01, 1.0])

    scroll_height_ratio = NumericProperty(4.0)
    rotation_scale = NumericProperty(1.0)

    spinner_width = NumericProperty(dp(40))

    disabled = BooleanProperty(False)

    def __init__(self, while_spinning_callback=None, **kwargs):
        self._is_spinning = False
        self._event = None
        self._while_spinning_callback = while_spinning_callback

        super(ExtendedThumbWheel, self).__init__(**kwargs)

        self.spacing = dp(3)
        self.label = _ColoredThumbWheelLabel(text='', color_tuple=('Brown', '700'),
                              size_hint_y=None, height=dp(60),)
        self.label.style = 'NavigationLabelSubHeading'

        thumbwheel_container = BoxLayout( size_hint=(None, None),
                                       size=(self.width, self.height-self.label.height - self.padding[3]), )

        self.thumbwheel = ThumbWheel( size_hint=(None, None),
                                      size=(self.width-dp(50), self.height-self.label.height - self.spacing[1] - self.padding[3]), )

        self.thumbwheel.value = self.thumbwheel.value_min

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

        self._being_set_externally = False
        self._last_value = None

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

    def set_value(self, value):
        if self._is_spinning:
            return
        self._being_set_externally = True
        self.value = value

    def update_value(self, instance, value):
        a = self.label_format % value
        self.label.text = self.label_text + ':\n' + a + ' ' + self.units
        self.value = value

        if self._last_value is None:
            self._last_value = float(value)
        diff = abs(value - self._last_value)
        comp = (self.value_max - self.value_min)/float(self.value_max)
        if diff < (comp*.00001):
            return
        self._last_value = float(value)
        if self._being_set_externally:
            self._being_set_externally = False
            if self._while_spinning_callback is not None:
                self._while_spinning_callback(value)
            return

        if self._while_spinning_callback is None:
            return

        if not self._is_spinning:
            self._is_spinning = True
            AppAwareThread(target=self._threaded_process, args=(instance, value,), show_busy=True).start()
        if self._event is not None:
            self._event.cancel()
        self._event = Clock.create_trigger(self._stop_process, 0.2)
        self._event()

    def _threaded_process(self, instance, value):
        if self._while_spinning_callback is None:
            self._is_spinning = False
            return
        while self._is_spinning:
            self._while_spinning_callback(value)
        self._stop_process()

    def _stop_process(self, *largs):
        self._is_spinning = False
        self._event = None

    def on_value(self, instance, value):
        self.thumbwheel.value = value

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
    num_segments = NumericProperty(30)

    spinner_width = NumericProperty(dp(40))

    def __init__(self, *largs, **kwargs):
        super(ThumbWheel, self).__init__(*largs, **kwargs)

        self.ht = self.height
        self.wd = self.width

        self.scrollview = ScrollView(size_hint=self.size_hint, size=self.size,
                                     bar_color=(.1,.3,.1,0.0),
                                     bar_inactive_color=(.3,.3,.1,0.0),
                                     )
        self.scrollview.effect_cls = ScrollEffect

        self.gridlayout = _ColoredGridLayout(cols=1, size_hint=(None, None), size=(self.width, 0))
        self.gridlayout.bind(minimum_height=self.gridlayout.setter('height'))

        self._scrolled_label = FlatLabel(text='', size_hint_y=None, height=self.ht * self.scroll_height_ratio)
        self.gridlayout.add_widget(self._scrolled_label)

        self.scrollview.add_widget(self.gridlayout)

        self.thumbwheel_widget = _ThumbWheelWidget(size_hint=self.size_hint, size=(self.spinner_width, self.height))
        self.ht_sum = 0
        self.labels = list()
        for i in range(self.num_segments):
            label = _ColoredThumbWheelLabel(text='', size_hint_y = None, height=400/20.0,
                             color_tuple=('Brown', '700'), font_size=dp(8),)
            #label.text = '%d' % i
            self.thumbwheel_widget.add_widget(label)
            self.labels.append(label)
            j = math.sin(i/float(self.num_segments) * 2*math.pi)
            ht = max(self.ht/self.num_segments * j,0)
            self.ht_sum += ht

        self.add_widget(self.scrollview)
        self.add_widget(self.thumbwheel_widget)

        self.thumbwheel_widget.center_x = self.scrollview.center_x
        self.scrollview.bind(scroll_y=self.on_scroll_y)
        self.on_scroll_y(self.scrollview, 1.0)

    def on_scroll_height_ratio(self, instance, value):
        self._scrolled_label.height = self.height * value

    def update_rotation(self, phase):
        phase = phase % (-1*math.pi)
        canvas_color = [0]*4
        for i in range(self.num_segments):
            label = self.labels[i]
            j = math.sin(i/float(self.num_segments) * 2*math.pi + phase)
            ht = max(self.ht/self.num_segments*j,0)
            label.height = ht * self.ht/self.ht_sum
            for ind in range(4):
                canvas_color[ind]  = self.color_max[ind] * abs(j)
                canvas_color[ind] += self.color_min[ind] * (1-abs(j))
            label.canvas_color = canvas_color

    def on_scroll_y(self, instance, value):
        value = min(max(value, 0), 1.0)
        self.update_rotation((value-1)*2*math.pi*self.rotation_scale)
        self.value = (1-value)*(self.value_max - self.value_min) + self.value_min

    def on_value(self, instance, value):
        self.scrollview.scroll_y = 1 - (value - self.value_min) / (self.value_max - self.value_min)
        #print('set scroll y to: %s' % str(self.scrollview.scroll_y))

    def on_color_max(self, instance, value):
        self.on_scroll_y(None, self.scrollview.scroll_y)

    def on_color_min(self, instance, value):
        self.on_scroll_y(None, self.scrollview.scroll_y)




