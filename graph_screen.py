
import itertools
from math import sin, cos, pi
from random import randrange

import numpy as np

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as rgb

from kivy.garden.graph import Graph, SmoothLinePlot, MeshLinePlot, BarPlot, MeshStemPlot, ContourPlot

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customgraphs import BarGraph, LineGraph

Builder.load_string('''
<-GardenGraphDemoScreen>:
    title: 'Graph Screen'
    theme: ('app', 'screen')
''')



class GardenGraphDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(GardenGraphDemoScreen, self).__init__(*largs, **kwargs)

        # example of a custom graph theme
        colors = itertools.cycle([
            rgb('dc7062'),
            rgb('66a8d4'),
            rgb('7dac9f'),
            rgb('e5b060'),
            ])
        graph_theme = {
            'font_size' : dp(9),
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            'background_color': rgb('f8f8f2'),  # back ground color of canvas
            'tick_color': (0, 0, 0, .2), # rgb('808080'),  # ticks and grid
            'border_color': rgb('808080')}  # border drawn around each graph

        graph = Graph(
            xlabel='Cheese',
            ylabel='Apples',
            x_ticks_minor=5,
            x_ticks_major=25,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            xmin=-50,
            xmax=50,
            ymin=-1,
            ymax=1,
            _with_stencilbuffer=False,
            **graph_theme
            )
            #background_color = (0.95, 0.95, 0.95, 1.0),

        plot = SmoothLinePlot(color=next(colors))
        plot.points = [(x / 10., sin(x / 50.)) for x in range(-500, 501)]
        # for efficiency, the x range matches xmin, xmax
        graph.add_plot(plot)

        plot = MeshLinePlot(color=next(colors))
        plot.points = [(x / 10., cos(x / 50.)) for x in range(-500, 501)]
        graph.add_plot(plot)
        self.plot = plot  # this is the moving graph, so keep a reference

        plot = MeshStemPlot(color=next(colors))
        graph.add_plot(plot)
        plot.points = [(x, x / 50.) for x in range(-50, 51)]

        plot = BarPlot(color=next(colors), bar_spacing=.72)
        graph.add_plot(plot)
        plot.bind_to_graph(graph)
        plot.points = [(x, .1 + randrange(10) / 10.) for x in range(-50, 1)]

        graph.size_hint_y = None
        graph.height = dp(150)
        self.add_widget(graph)

        #Clock.schedule_interval(self.update_points, 1 / 10.0)
        # self.update_points(None)

        graph2 = Graph(
            xlabel='Position (m)',
            ylabel='Time (s)',
            x_ticks_minor=0,
            x_ticks_major=1,
            y_ticks_major=10,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            xmin=0,
            ymin=0,
            _with_stencilbuffer=False,
            **graph_theme)

        (xbounds, ybounds, data) = self.make_contour_data()
        # This is required to fit the graph to the data extents
        graph2.xmin, graph2.xmax = xbounds
        graph2.ymin, graph2.ymax = ybounds

        plot = ContourPlot()
        plot.data = data
        plot.xrange = xbounds
        plot.yrange = ybounds
        plot.color = [1, 0.7, 0.2, 1]
        graph2.add_plot(plot)

        graph2.size_hint_y = None
        graph2.height = dp(150)
        self.add_widget(graph2)
        self.contourplot = plot

        #Clock.schedule_interval(self.update_contour, 1 / 10.)
        self.update_contour(None)

    def on_enter(self, *largs):
        print 'in on enter...'
        Clock.schedule_interval(self.update_points, 1/10.0)
        Clock.schedule_interval(self.update_contour, 1 / 10.)

    def on_pre_leave(self, *largs):
        print 'in on pre leave...'
        Clock.unschedule(self.update_points)
        Clock.unschedule(self.update_contour)

    def make_contour_data(self, ts=0):
        omega = 2 * pi / 30
        k = (2 * pi) / 2.0

        ts = sin(ts * 2) + 1.5  # emperically determined 'pretty' values
        npoints = 100
        data = np.ones((npoints, npoints))

        position = [ii * 0.1 for ii in range(npoints)]
        time = [(ii % 100) * 0.6 for ii in range(npoints)]

        for ii, t in enumerate(time):
            for jj, x in enumerate(position):
                data[ii, jj] = sin(k * x + omega * t) + sin(-k * x + omega * t) / ts
        return ((0, max(position)), (0, max(time)), data)

    def update_points(self, *args):
        # print 'updating points'
        self.plot.points = [(x / 10., cos(Clock.get_time() + x / 50.)) for x in range(-500, 501)]


    def update_contour(self, *args):
        _, _, self.contourplot.data[:] = self.make_contour_data(Clock.get_time())
        # this does not trigger an update, because we replace the
        # values of the arry and do not change the object.
        # However, we cannot do "...data = make_contour_data()" as
        # kivy will try to check for the identity of the new and
        # old values.  In numpy, 'nd1 == nd2' leads to an error
        # (you have to use np.all).  Ideally, property should be patched
        # for this.
        self.contourplot.ask_draw()



