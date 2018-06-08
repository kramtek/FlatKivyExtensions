
import itertools, math
from math import sin, cos, pi, log10
from random import randrange

import numpy as np

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as rgb

from flat_kivy_extensions.uix.customscreen import CustomScreen

from kivy.garden.graph import Graph, SmoothLinePlot, MeshLinePlot, BarPlot, MeshStemPlot, ContourPlot, LinePlot
from kivy.properties import ListProperty

Builder.load_string('''
<-GraphDemoScreen>:
    title: 'Graph Screen'
    theme: ('app', 'screen')
''')


def identity(x):
    return x



class _CustomGraph(Graph):
    x_tick_labels = ListProperty([], allownone=True)

    def update_x_tick_labels(self, instance, value):
        self._update_labels()

    def _update_labels(self):
        result = super(_CustomGraph, self)._update_labels()
        xlabels = self._x_grid_label
        ylabels = self._y_grid_label
        maxWidth = 0
        if len(self.x_tick_labels) > 0:
            for (index, xlabel) in enumerate(xlabels):
                if len(self.x_tick_labels) > index:
                    xlabel.text = self.x_tick_labels[index]
                else:
                    xlabel.text = ''

                if self.x_ticks_angle > 0:
                    xlabel.texture_update()
                    size = xlabel.texture_size
                    print 'size: %s' % str(size)
                    if (size[0]) > maxWidth:
                        maxWidth = size[0]
            print 'maxWidth: %s ' % str(maxWidth)
            for xlabel in xlabels:
                w = xlabel.texture_size[0]
                xlabel.pos = (xlabel.pos[0], xlabel.pos[1] + maxWidth/2.0 + (maxWidth - w)/2.0)

            if self.x_ticks_angle > 0:
            #if False:
                funclog = log10 if self.ylog else identity
                ypoints = self._ticks_majory
                x_next = self.padding + self.x
                ylabel = self._ylabel
                if ylabel:
                    x_next += self.padding + ylabel.height
                y_next = self.padding + self.y + 20
                for (k, ylabel) in enumerate(ylabels):
                    y1 = ylabel.texture_size
                    y_start = y_next + (self.padding + y1[1] if len(xlabels) and self.x_grid_label
                                    else 0) + (self.padding + y1[1] if not y_next else 0)

                    yextent = self.y + self.height - self.padding - y1[1] / 2. - maxWidth
                    ymin = funclog(self.ymin)

                    ratio = (yextent - y_start) / float(funclog(self.ymax) - ymin)
                    y_start -= y1[1] / 2.
                    y1 = y1[0]
                    ylabel.pos = (
                        int(x_next),
                        int(y_start + (ypoints[k] - ymin) * ratio) + maxWidth)

                ylabel = self._ylabel
                if ylabel:
                    ylabel.y = int(ylabel.y + maxWidth/2)

        return (result[0], result[1]+maxWidth, result[2], result[3])



class LineGraph(_CustomGraph):

    def __init__(self, *largs, **kwargs):
        super(LineGraph, self).__init__(*largs, **kwargs)
        self._plots = list()

    def create(self, data):
        colors = itertools.cycle([
            rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])

        self.shape = data.shape
        numPoints = self.shape[0]
        self.xmin = 1.0
        self.xmax = numPoints
        print 'xmax: %s' % str(self.xmax)
        if self.x_ticks_major == 0:
            self.x_ticks_major=self.xmax

        for ind1 in xrange(self.shape[1]):
            plot = LinePlot(color=next(colors))
            plot.line_width = dp(1)
            self.add_plot(plot)
            self._plots.append(plot)
            plot.points = [(x+self.xmin, data[x,ind1])  for x in xrange(numPoints)]

    def update(self, data):
        if self.shape != self.shape:
            self.create(data)
        for ind1 in xrange(self.shape[1]):
            plot = self._plots[ind1]
            plot.points = [(x+self.xmin, data[x,ind1])  for x in xrange(self.shape[0])]


class BarGraph(_CustomGraph):

    def __init__(self, *largs, **kwargs):
        super(BarGraph, self).__init__(*largs, **kwargs)
        self._plots = list()
        self._plot_datas = list()
        self.bind(x_tick_labels=self.update_x_tick_labels)

    def create(self, data):
        colors = itertools.cycle([
            rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])

        self.shape = data.shape
        numPoints = self.shape[0] * (1 + self.shape[1])
        self.xmin = 0.0
        self.xmax = self.shape[0] + 1
        self.x_ticks_minor = 1
        self.x_ticks_major=1
        print ' shape: %s'  % str(self.shape)
        scaling = float(1.0/float(self.shape[1]+1))

        width   = float(1.0/float(self.shape[1]+1))

        ratio = float(self.shape[0])/float(self.shape[1])
        if numPoints == 2:
            spacing = 0.9
        else:
            if ratio >= 1:
                spacing = 0.8
            else:
                spacing = 0.7

        for ind1 in xrange(self.shape[1]):
            plot = BarPlot(color=next(colors), bar_spacing=spacing)
            self.add_plot(plot)
            plot.bind_to_graph(self)
            self._plots.append(plot)
            plot_data = [((x*scaling) + width*(float(self.shape[1])/2.0) + 0.0*(float(self.shape[1])/float(self.shape[1]+1)), 0.0) for x in range(0, numPoints+1)]
            self._plot_datas.append(plot_data)
            for ind2 in xrange(self.shape[0]):
                index = ind1 + 1 + ind2*(self.shape[1]+1)
                plot_data[index] = (plot_data[index][0], data[ind2,ind1])
            plot.points = plot_data

    def update(self, data):
        if self.shape != data.shape:
            self.create(data)
        for ind1 in xrange(self.shape[1]):
            plot = self._plots[ind1]
            plot_data = self._plot_datas[ind1]
            for ind2 in xrange(self.shape[0]):
                index = ind1 + 1 + ind2*(self.shape[1]+1)
                plot_data[index] = (plot_data[index][0], data[ind2,ind1])
            plot.points = plot_data





class GraphDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(GraphDemoScreen, self).__init__(*largs, **kwargs)

        # example of a custom graph theme
        colors = itertools.cycle([
            rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])
        graph_theme = {
            'font_size' : dp(9),
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            # 'background_color': rgb('f8f8f2'),  # back ground color of canvas
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
        graph.height = dp(100)
        self.add_widget(graph)




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
        self.dataShape = (3,4)
        self.barGraph.create(np.random.random( self.dataShape ) * 100)

        # Override the default labels and label rotation
        self.barGraph.x_ticks_angle = 270
        self.barGraph.x_tick_labels = ['', 'apples', 'oranges', 'peaches', '']
        #self.barGraph.x_tick_labels = ['', 'a', 'o', 'p', '']
        #self.barGraph.x_tick_labels = ['', 'abc', 'def', '123', 'hij', '3']

        self.barGraph.size_hint_y = None
        self.barGraph.height = dp(140)
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
        self.lineGraph.height = dp(100)
        self.add_widget(self.lineGraph)


        Clock.schedule_interval(self.update_points, 1 / 10.0)
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
        graph2.height = dp(100)
        self.add_widget(graph2)
        self.contourplot = plot

        Clock.schedule_interval(self.update_contour, 1 / 10.)
        self.update_contour(None)


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
        self.plot.points = [(x / 10., cos(Clock.get_time() + x / 50.)) for x in range(-500, 501)]

        data = np.random.random( self.dataShape ) * 100
        self.barGraph.update(data)

        data = np.random.random( (10,4)) * 10 - 1.5

        self.lineGraph.update(data)

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



