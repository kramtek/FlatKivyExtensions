
import math, time, threading

import numpy as np

from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as rgb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.effects.scroll import ScrollEffect

from kivy.properties import NumericProperty, ListProperty, StringProperty

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customgraphs import BarGraph, LineGraph
from flat_kivy.uix.flatlabel import FlatLabel


Builder.load_string('''
<-GraphDemoScreen>:
    title: 'Graph Screen'
    theme: ('app', 'screen')

<-TestScreen>:
    title: 'Test Screen'
    theme: ('app', 'screen')




<-ExtendedThumbWheel>:
    cols: 1
    canvas.before:
        Color:
            rgba: (4.0, 0.5, 0.4, 0.0)
        Rectangle:
            size: self.size
            pos: self.pos




<_ColoredLabel>:
    canvas_color: (.8, 0.9, .8, 0.0)
    #style: 'NavigationLabelSubHeading'
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
            rgba: (0.4, 0.5, 0.4, 0.9)
        Rectangle:
            size: self.size
            pos: self.pos


''')

class GraphDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(GraphDemoScreen, self).__init__(*largs, **kwargs)

        graph_theme = {
            'font_size' : dp(9),
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            'background_color': rgb('f8f8f2'),  # back ground color of canvas
            'tick_color': (0, 0, 0, .2), # rgb('808080'),  # ticks and grid
            'border_color': rgb('808080')}  # border drawn around each graph

        self.barGraph = BarGraph(
            xlabel='Fruit',
            ylabel='Amount (%)',
            y_ticks_major=25,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            # These are overriden in the custom BarGraph
            #xmin=0,
            #xmax=50,
            #x_ticks_minor=5,
            #x_ticks_major=25,
            ymin=0,
            ymax=100,
            _with_stencilbuffer=False,
            **graph_theme
            )
        self.dataShape = (3,6)
        self.barGraph.create(np.random.random( self.dataShape ) * 100)

        # Override the default labels and label rotation
        self.barGraph.x_ticks_angle = 270
        self.barGraph.x_tick_labels = ['', 'apples', 'oranges', 'peaches', '']
        #self.barGraph.x_tick_labels = ['', 'a', 'o', 'p', '']
        #self.barGraph.x_tick_labels = ['', 'abc', 'def', '123', 'hij', '3']

        self.barGraph.size_hint_y = None
        self.barGraph.height = dp(180)
        self.add_widget(self.barGraph)


        self.lineGraph = LineGraph(
            xlabel='Data',
            ylabel='Score',
            y_ticks_major=2,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            # These are overriden in the custom BarGraph
            #xmin=0,
            #xmax=50,
            #x_ticks_minor=5,
            x_ticks_major=2,
            ymin=-2,
            ymax=9,
            _with_stencilbuffer=False,
            **graph_theme
            )
        dataShape = (50,4)
        self.lineGraph.create(np.random.random(dataShape ) * 10 - 1.5)

        #self.lineGraph.x_ticks_angle = 270
        #self.lineGraph.x_tick_labels = ['', 'a', 'b', 'c', '']

        self.lineGraph.size_hint_y = None
        self.lineGraph.height = dp(150)
        self.add_widget(self.lineGraph)

        Clock.schedule_interval(self.update_points, 1 / 10.0)

    def update_points(self, *args):

        data = np.random.random( self.dataShape ) * 100
        self.barGraph.update(data)

        data = np.random.random( (50,4)) * 10 - 1.5
        self.lineGraph.update(data)



class _ColoredLabel(FlatLabel):
    pass


class ExtendedThumbWheel(GridLayout):
    label_text = StringProperty('Label')
    label_format = StringProperty('%2.3f')
    units = StringProperty('')

    value = NumericProperty(None, allownone=True)
    value_max = NumericProperty(1.0)
    value_min = NumericProperty(0.0)
    color = ListProperty([.3, .4, .3, 0.5])

    def __init__(self, *largs, **kwargs):
        super(ExtendedThumbWheel, self).__init__(*largs, **kwargs)

        self.label = _ColoredLabel(text='', color_tuple=('Brown', '700'),
                              size_hint_y=None, height=dp(45),)
        self.label.style = 'NavigationLabelSubHeading'

        thumbwheel_container = BoxLayout( size_hint=(None, None),
                                       size=(dp(200), self.height-self.label.height), )

        self.thumbwheel = ThumbWheel( size_hint=(None, None),
                                      size=(dp(40), self.height-self.label.height), )

        self.thumbwheel.value = self.thumbwheel.value_min

        self.bind(value_min=self.thumbwheel.setter('value_min'))
        self.bind(value_max=self.thumbwheel.setter('value_max'))
        self.bind(color=self.thumbwheel.setter('color'))

        thumbwheel_container.add_widget(Widget())
        thumbwheel_container.add_widget(self.thumbwheel)
        thumbwheel_container.add_widget(Widget())

        self.add_widget(thumbwheel_container)
        self.add_widget(self.label)

        self.thumbwheel.bind(value=self.update_value)

    def update_value(self, instance, value):
        a = self.label_format % value
        self.label.text = self.label_text + ':\n' + a + ' ' + self.units
        self.value = value

    def on_value(self, instance, value):
        self.thumbwheel.value = value


class _ThumbWheelWidget(BoxLayout):
    pass


class ThumbWheel(RelativeLayout):

    value = NumericProperty(None, allownone=True)
    value_max = NumericProperty(1.0)
    value_min = NumericProperty(0.0)
    color_max = ListProperty([.6, .8, .6, 1.0])
    color_min = ListProperty([.01, .01, .01, 1.0])

    def __init__(self, *largs, **kwargs):
        super(ThumbWheel, self).__init__(*largs, **kwargs)


        self.num_labels = 30
        self.ht = self.height
        self.wd = self.width
        self.num_labels_showing = 5.0

        self.scrollview = ScrollView(size_hint=self.size_hint, size = self.size,
                                     bar_color=(.1,.3,.1,0.0),
                                     bar_inactive_color=(.3,.3,.1,0.0),
                                     )
        self.scrollview.effect_cls = ScrollEffect

        self.gridlayout = GridLayout(cols=1, size_hint=(None, None), size=(self.size[0], 0))
        self.gridlayout.bind(minimum_height=self.gridlayout.setter('height'))

        label = FlatLabel(text='', size_hint_y=None, height=self.ht/self.num_labels_showing*self.num_labels)
        self.gridlayout.add_widget(label)

        self.scrollview.add_widget(self.gridlayout)

        self.thumbwheel_widget = _ThumbWheelWidget(size_hint=self.size_hint, size=self.size)
        self.nb2 = 30
        self.ht_sum = 0
        self.labels3 = list()
        for i in range(self.nb2):
            label = _ColoredLabel(text='', size_hint_y = None, height=400/20.0,
                             color_tuple=('Brown', '700'), font_size=dp(8),)
            label.text = '%d' % i
            self.thumbwheel_widget.add_widget(label)
            self.labels3.append(label)
            j = math.sin(i/float(self.nb2) * 2*math.pi)
            ht = max(self.ht/self.nb2 * j,0)
            self.ht_sum += ht

        self.add_widget(self.thumbwheel_widget)
        self.add_widget(self.scrollview)

        self.scrollview.bind(scroll_y=self.on_scroll_y)
        self.on_scroll_y(self.scrollview, 1.0)

    def update_rotation(self, phase):
        for i in range(self.nb2):
            label = self.labels3[i]
            j = math.sin(i/float(self.nb2) * 2*math.pi + phase)
            ht = max(self.ht/self.nb2*j,0)
            label.height = ht * self.ht/self.ht_sum
            canvas_color = [0]*4
            for ind in range(4):
                canvas_color[ind]  = self.color_max[ind] * abs(j)
                canvas_color[ind] += self.color_min[ind] * (1-abs(j))
            label.canvas_color = canvas_color

    def on_scroll_y(self, instance, value):
        value = min(max(value, 0), 1.0)
        self.update_rotation((value-1)*2*math.pi/2.0/1.0)
        self.value = (1-value)*(self.value_max - self.value_min) + self.value_min

    def on_value(self, instance, value):
        self.scrollview.scroll_y = 1 - (value - self.value_min) / (self.value_max - self.value_min)




class TestScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(TestScreen, self).__init__(*largs, **kwargs)

        self._isRunning = False
        self.event = None

        extended_thumbwheel = ExtendedThumbWheel( size_hint=(None, None), size=(dp(200), dp(200)),)
        extended_thumbwheel.label_text = 'MyValue'
        extended_thumbwheel.label_format = '%2.1f'
        extended_thumbwheel.units = 'Space Credits'
        extended_thumbwheel.value_max = 19
        extended_thumbwheel.value_min = 3
        extended_thumbwheel.bind(value=self.thumbwheel_updated_value)
        self.add_widget(extended_thumbwheel)

        extended_thumbwheel.value = 4.4

    def thumbwheel_updated_value(self, instance, value):
        # If it is not already running then start a thread in the background
        # to make the updates when it can and assign a trigger to
        # stop the thread after Xyz seconds
        if not self._isRunning:
            threading.Thread(target=self._threaded_process).start()
        if self.event is not None:
            self.event.cancel()
        self.event = Clock.create_trigger(self._stop_process, 0.5)
        self.event()

    def _stop_process(self, *largs):
        self._isRunning = False
        self.event = None

    def _threaded_process(self):
        self._isRunning = True
        App.get_running_app().indicate_busy(True)
        while self._isRunning:
            time.sleep(0.2)
            #print '  will write to somewhere, current value: %2.2f' % self.thumbwheel.value
        self._stop_process()
        App.get_running_app().indicate_busy(False)






    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print '%s got double tapped' % str(self)
            App.get_running_app().raise_error('Touch input:', 'Double tap received...',
                                          auto_dismiss=False)
        return super(TestScreen, self).on_touch_down(touch)



