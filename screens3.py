import time

import numpy as np

from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as rgb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from flat_kivy_extensions import AppAwareThread
from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customgraphs import BarGraph, LineGraph
from flat_kivy_extensions.uix.custombutton import CustomButton
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
            'font_size': dp(9),
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            'background_color': rgb('f8f8f2'),  # back ground color of canvas
            'tick_color': (0, 0, 0, .2),  # rgb('808080'),  # ticks and grid
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
            # xmin=0,
            # xmax=50,
            # x_ticks_minor=5,
            # x_ticks_major=25,
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
        # self.barGraph.x_tick_labels = ['', 'a', 'o', 'p', '']
        # self.barGraph.x_tick_labels = ['', 'abc', 'def', '123', 'hij', '3']

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
            # These are overridden in the custom BarGraph
            # xmin=0,
            # xmax=50,
            # x_ticks_minor=5,
            x_ticks_major=2,
            ymin=-2,
            ymax=9,
            _with_stencilbuffer=False,
            line_width=dp(1.25),
            **graph_theme
        )
        #        dataShape = (50,4)
        #        self.lineGraph.create(np.random.random(dataShape ) * 10 - 1.5)

        # self.lineGraph.x_ticks_angle = 270
        # self.lineGraph.x_tick_labels = ['', 'a', 'b', 'c', '']

        self.lineGraph.size_hint_y = None
        self.lineGraph.height = dp(150)
        self.add_widget(self.lineGraph)

        # Clock.schedule_interval(self.update_points, 1 / 10.0)

        App.get_running_app().register_stop_callback(self.app_stopping)

    def app_stopping(self):
        print('App is stopping - should sut down any open threads...')

    def on_enter(self, *largs):
        Clock.schedule_interval(self.update_points, 1 / 10.0)

    def on_pre_leave(self, *largs):
        Clock.unschedule(self.update_points)

    def update_points(self, *args):
        data = np.random.random((3, 6)) * 100
        self.barGraph.update(data)
        data = np.random.random((50, 4)) * 10 - 1.5
        self.lineGraph.update(data)


class ThumbwheelScreen(CustomScreen):
    def __init__(self, *largs, **kwargs):
        super(ThumbwheelScreen, self).__init__(*largs, **kwargs)

        self._isRunning = False
        self.event = None

        bl = BoxLayout(size_hint_y=None, height=dp(300))

        extended_thumbwheel = ExtendedThumbWheel(size_hint=(None, None), size=(dp(150), dp(300)),
                                                 while_spinning_callback=self._while_spinning_callback)

        extended_thumbwheel.label_text = 'MyValue'
        extended_thumbwheel.label_format = '%2.1f'
        extended_thumbwheel.units = 'Space Credits'
        extended_thumbwheel.value_max = 19
        extended_thumbwheel.value_min = 3
        extended_thumbwheel.spinner_width = dp(40)
        # self.add_widget(extended_thumbwheel)
        bl.add_widget(Widget())
        bl.add_widget(extended_thumbwheel)

        # extended_thumbwheel.value = 4.4
        # extended_thumbwheel.value = 19
        extended_thumbwheel.set_value(19)
        extended_thumbwheel.rotation_scale = 4.0

        extended_thumbwheel.disabled = True
        self.et = extended_thumbwheel

        extended_thumbwheel = ExtendedThumbWheel(size_hint=(None, None), size=(dp(150), dp(300)),
                                                 while_spinning_callback=self._while_spinning_callback)
        extended_thumbwheel.label_text = 'MyValue2'
        extended_thumbwheel.label_format = '%2.1f'
        extended_thumbwheel.units = 'Space Credits'
        extended_thumbwheel.value_max = 19
        extended_thumbwheel.value_min = -2

        # extended_thumbwheel.value = 4.4
        extended_thumbwheel.set_value(4.4)
        extended_thumbwheel.rotation_scale = 0.5
        extended_thumbwheel.color_max = [.9, .9, .8, 1.0]
        extended_thumbwheel.color_min = [.01, .01, .01, 1.0]

        extended_thumbwheel.scroll_height_ratio = 12.0
        # self.add_widget(extended_thumbwheel)
        bl.add_widget(extended_thumbwheel)
        self.add_widget(bl)
        self.et2 = extended_thumbwheel

        btn = CustomButton(text='set', size_hint=(None, None), size=(dp(150), dp(50)))
        btn.theme = ('app', 'default')
        btn.bind(on_release=self._set_value)
        self.add_widget(btn)

        App.get_running_app().register_stop_callback(self.app_stopping)

    def _set_value(self, *largs):
        print('setting thumbwheel value...')
        # self.et.set_value(5.6)
        AppAwareThread(target=self._set_value_2).start()

    def _set_value_2(self, *largs):
        # self.et.set_value(5.6 + 0/20.0*2.0)
        # time.sleep(0.1)
        for index in xrange(10):
            # self.et.set_value(5.6 + index/20.0*0.5)
            # self.et.on_value( self, 5.6 + index/20.0*0.5 )
            self.et.set_value(5.6 + index / 10.0 * 1.0)
            self.et2.set_value(5.6 + index / 10.0 * 1.0)
            time.sleep(0.3)

    def _while_spinning_callback(self, value):
        print '  will write to somewhere, current value: %2.2f' % value
        time.sleep(0.1)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print '%s got double tapped' % str(self)
            App.get_running_app().raise_error('Touch input:', 'Double tap received...',
                                              auto_dismiss=False)
        return super(ThumbwheelScreen, self).on_touch_down(touch)

    def app_stopping(self):
        print('Application stopping - stop back ground process(es)')

    def _un_disable(self, *largs):
        self.et.disabled = False

    def on_enter(self):
        _event = Clock.create_trigger(self._un_disable, 5.0)
        _event()
