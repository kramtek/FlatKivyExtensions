
from kivy.lang import Builder
import numpy as np

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as rgb

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customgraphs import BarGraph, LineGraph

Builder.load_string('''
<-GraphDemoScreen>:
    title: 'Graph Screen'
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
        dataShape = (10,4)
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

        data = np.random.random( (10,4)) * 10 - 1.5
        self.lineGraph.update(data)


