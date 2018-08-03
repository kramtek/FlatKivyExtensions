
import time, threading

import numpy as np

from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as rgb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customgraphs import BarGraph, LineGraph
from flat_kivy_extensions.uix.thumbwheel import ExtendedThumbWheel

Builder.load_string('''
<-GraphDemoScreen>:
    title: 'Graph Screen'
    theme: ('app', 'screen')

<-ThumbwheelScreen>:
    title: 'Thumb Wheels'
    theme: ('app', 'screen')

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
#        self.dataShape = (3,6)
#        self.barGraph.create(np.random.random( self.dataShape ) * 100)

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
            line_width=dp(1.25),
            **graph_theme
            )
#        dataShape = (50,4)
#        self.lineGraph.create(np.random.random(dataShape ) * 10 - 1.5)

        #self.lineGraph.x_ticks_angle = 270
        #self.lineGraph.x_tick_labels = ['', 'a', 'b', 'c', '']

        self.lineGraph.size_hint_y = None
        self.lineGraph.height = dp(150)
        self.add_widget(self.lineGraph)

        #Clock.schedule_interval(self.update_points, 1 / 10.0)

        App.get_running_app().register_stop_callback(self.app_stopping)

    def app_stopping(self):
        print('App is stopping - should sut down any open threads...')

    def on_enter(self, *largs):
        Clock.schedule_interval(self.update_points, 1/10.0)

    def on_pre_leave(self, *largs):
        Clock.unschedule(self.update_points)

    def update_points(self, *args):
        data = np.random.random( (3,6) ) * 100
        self.barGraph.update(data)
        data = np.random.random( (50,4) ) * 10 - 1.5
        self.lineGraph.update(data)



class ThumbwheelScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(ThumbwheelScreen, self).__init__(*largs, **kwargs)

        self._isRunning = False
        self.event = None

        bl = BoxLayout(size_hint_y=None, height=dp(300))

        extended_thumbwheel = ExtendedThumbWheel( size_hint=(None, None), size=(dp(150), dp(300)),)
        extended_thumbwheel.label_text = 'MyValue'
        extended_thumbwheel.label_format = '%2.1f'
        extended_thumbwheel.units = 'Space Credits'
        extended_thumbwheel.value_max = 19
        extended_thumbwheel.value_min = 3
        extended_thumbwheel.bind(value=self.thumbwheel_updated_value)
        extended_thumbwheel.spinner_width = dp(40)
        #self.add_widget(extended_thumbwheel)
        bl.add_widget(Widget())
        bl.add_widget(extended_thumbwheel)

        extended_thumbwheel.value = 4.4
        extended_thumbwheel.rotation_scale = 4.0

        extended_thumbwheel = ExtendedThumbWheel( size_hint=(None, None), size=(dp(150), dp(300)),)
        extended_thumbwheel.label_text = 'MyValue2'
        extended_thumbwheel.label_format = '%2.1f'
        extended_thumbwheel.units = 'Space Credits'
        extended_thumbwheel.value_max = 19
        extended_thumbwheel.value_min = -2

        extended_thumbwheel.value = 4.4
        extended_thumbwheel.rotation_scale = 0.5
        extended_thumbwheel.color_max = [.9, .9, .8, 1.0]
        extended_thumbwheel.color_min = [.01, .01, .01, 1.0]

        #self.add_widget(extended_thumbwheel)
        bl.add_widget(extended_thumbwheel)
        self.add_widget(bl)


    def thumbwheel_updated_value(self, instance, value):
        # If it is not already running then start a thread in the background
        # to write the update values when it can and assign a trigger to
        # stop the thread after 0.5 seconds. If the value is updated
        # within the timeout period the timeout event is rescheduled
        if not self._isRunning:
            threading.Thread(target=self._threaded_process, args=(instance, value,)).start()
        if self.event is not None:
            self.event.cancel()
        self.event = Clock.create_trigger(self._stop_process, 0.5)
        self.event()

    def _stop_process(self, *largs):
        self._isRunning = False
        self.event = None

    def _threaded_process(self, instance, value):
        self._isRunning = True
        App.get_running_app().indicate_busy(True)
        while self._isRunning:
            time.sleep(0.2)
            print '  will write to somewhere, current value: %2.2f' % instance.value
        self._stop_process()
        App.get_running_app().indicate_busy(False)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print '%s got double tapped' % str(self)
            App.get_running_app().raise_error('Touch input:', 'Double tap received...',
                                          auto_dismiss=False)
        return super(ThumbwheelScreen, self).on_touch_down(touch)



