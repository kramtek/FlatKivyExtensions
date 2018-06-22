

import itertools
from math import log10

from kivy.metrics import dp
from kivy.utils import get_color_from_hex as rgb
from kivy.properties import ListProperty
from kivy.garden.graph import Graph, BarPlot, LinePlot


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
                    if (size[0]) > maxWidth:
                        maxWidth = size[0]
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
            rgb('66a8d4'),
            rgb('dc7062'),
            rgb('7dac9f'),
            rgb('e5b060'),
            ])

        self.shape = data.shape
        numPoints = self.shape[0]
        self.xmin = 1.0
        self.xmax = numPoints
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

    def create(self, data, colors=None):
        if colors is None:
            colors = itertools.cycle([
                rgb('66a8d4'),
                rgb('dc7062'),
                rgb('e5b060'),
                rgb('7dac9f'),
                ])

        self.shape = data.shape
        numPoints = self.shape[0] * (1 + self.shape[1])
        self.xmin = 0.0
        self.xmax = self.shape[0] + 1
        self.x_ticks_minor = 1
        self.x_ticks_major=1
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



