
import itertools
from kivy.utils import get_color_from_hex as rgb
from math import sin, cos, pi
from random import randrange
import numpy as np

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen

from kivy.garden.graph import Graph, SmoothLinePlot, MeshLinePlot, MeshStemPlot, ContourPlot

from flat_kivy_extensions.uix.customscreen import CustomScreen

from flat_kivy_extensions.uix.customlayouts import StyledLayout, GroupedLayout
from flat_kivy_extensions.uix.dropshadow import DropShadow
from flat_kivy_extensions.uix.custombutton import CustomButton
from flat_kivy_extensions.uix.customcheckbox import CustomCheckBoxListItem

Builder.load_string('''
<-KivyWidgetScreen>:
    title: 'Basic Custom Screen'
    theme: ('app', 'screen')

    Label:
        text: 'CustomScreen = \\n HeaderLabel + GridLayout'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

    Label:
        text: 'add_widget() for screen is forwarded \\n to the content (grid) layout'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

    Label:
        text: 'Number of columns in the grid layout depends\\n on the screen orientation'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

    Label:
        text: 'Portrait: cols: 1\\nLandscape: cols=2'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

    Label:
        text: 'Examples of stock Widgets \\nin custom screen in StackLayout'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

    Button:
        text: 'button'
        size_hint: None, None
        size: '130dp', '60dp'

    Slider:
        size_hint: None, None
        size: '200dp', '50dp'
        orientation: 'horizontal'

    Switch:
        size_hint_y: None
        height: '50dp'

        on_parent: root.done_building()

<-CustomButtonDemoScreen>:
    title: 'Custom Buttons'
    theme: ('app', 'screen')

    CustomButton:
        text: 'Custom Button #1'
        theme: ('app', 'default')
        size_hint: None, None
        size: dp(200), dp(60)

    CustomButton:
        text: 'Custom Button #2 (no theme)'
        #theme: ('app', 'default')
        size_hint: None, None
        size: dp(110), dp(150)
        radius: '25dp'
        font_color_tuple: ('Blue', '100')
        font_size: '20dp'

    CustomButton:
        text: 'Custom Button #3'
        theme: ('app', 'default')
        size_hint: None, None
        size: dp(200), dp(40)
        radius: '4dp'
        color_tuple: ('Green', '800')

    CustomButton:
        text: 'CoverFlow Navigation'
        theme: ('app', 'default')
        size_hint: None, None
        size: dp(250), dp(40)
        radius: '4dp'
        color_tuple: ('Blue', '800')
        on_release: root.show_popup()

<-CustomCheckBoxDemoScreen>:
    title: 'Custom Checkboxes'
    theme: ('app', 'screen')

    CustomCheckBoxListItem:
        text: 'Check box'
        theme: ('app', 'default')
        height: '50dp'

    CustomCheckBoxListItem:
        text: 'Radio Button 1'
        group: 'this-radio'
        theme: ('app', 'default')
        height: '50dp'

        radius: '12dp'
        check_scale: .25
        icon: 'fa-circle'
        check_color_tuple: ('Brown', '500')
        check_color_hue_down: '300'
        outline_color_tuple: ('Blue', '500')

        size_scaling: 0.5

        exclusive: True


    CustomCheckBoxListItem:
        text: 'Radio Button 2'
        group: 'this-radio'
        theme: ('app', 'default')
        height: '50dp'

        radius: '12dp'
        check_scale: .25
        icon: 'fa-circle'
        check_color_tuple: ('Brown', '500')
        check_color_hue_down: '300'
        outline_color_tuple: ('Blue', '500')

        size_scaling: 0.5

        exclusive: True

        current_state: True



    CustomCheckBoxListItem:
        text: 'Error Indicator'
        theme: ('app', 'default')
        height: '50dp'
        icon: 'fa-exclamation'
        check_color_tuple: ('Red', '500')
        outline_color_tuple: ('Gray', '500')

    CustomCheckBoxListItem:
        text: 'Warning Indicator'
        theme: ('app', 'default')
        height: '50dp'
        icon: 'fa-warning'
        check_color_tuple: ('Yellow', '800')
        outline_color_tuple: ('Gray', '500')
        check_scale: .4
        on_active: if self.active: print('warning activated')
        current_state: True
        radius: '1dp'
        outline_color_tuple: ('Gray', '900')
        outline_size: '0.5dp'

    CustomCheckBoxListItem:
        text: 'Exception Indicator'
        theme: ('app', 'default')
        height: '50dp'
        icon: 'fa-times'
        check_color_tuple: ('Red', '500')
        outline_color_tuple: ('Gray', '500')

<-CustomSliderDemoScreen>:
    title: 'Custom Sliders'
    theme: ('app', 'screen')

    CustomSlider:
        orientation: 'horizontal'
        min: 10
        max: 110
        theme: ('green', 'main')
        size_hint_y: None
        height: '50dp'

    CustomSlider:
        orientation: 'vertical'
        min: 10
        max: 110
        theme: ('green', 'main')
        height: '200dp'
        size_hint_y: None

    ExtendedSlider:
        orientation: 'horizontal'
        size_hint_y: None
        height: '100dp'
        label_text: 'Value'
        theme: ('green', 'main')


    BoxLayout:
        size_hint_y: None
        height: '200dp'

        ExtendedSlider:
            orientation: 'vertical'
            size_hint_y: None
            height: '280dp'
            label_text: 'VertValue1'
            units: 'ms'
            max: 30
            min: 20
            label_format: '%1.1f'
            theme: ('green', 'main')

        ExtendedSlider:
            orientation: 'vertical'
            size_hint_y: None
            height: '280dp'
            label_text: 'VertValue2'
            units: 'volts'
            max: 60
            min: 40
            label_format: '%1.2f'
            theme: ('green', 'main')


<-CustomLayoutsScreen>:
    title: 'Another Custom Screen'
    theme: ('app', 'screen')

<-DropShadowScreen>:
    title: 'Drop Shadows'
    theme: ('app', 'screen')
    spacing: '1dp'

    # Button:
    #     text: 'button'
    #     size_hint_y: None
    #     height: '50dp'
    #
    # DropShadow:
    #     blur_radius: 2
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)
    #
    # DropShadow:
    #     blur_radius: 4
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)
    #
    # DropShadow:
    #     blur_radius: 8
    #     offset_scaling: 0.5
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)
    #
    # DropShadow:
    #     blur_radius: 8
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)

<-CustomGraphScreen>:

''')


class KivyWidgetScreen(CustomScreen):
    pass

    def done_building(self):
        self.dropdown = DropDown()
        for index in range(10):
            btn = Button(text='Value %d' % index, size_hint_y=None, height=dp(35))
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        mainbutton = Button(text='Select one', size_hint=(None, None))
        mainbutton.size = (dp(200), dp(40))
        mainbutton.bind(on_release=self.dropdown.open)
        self.add_widget(mainbutton)

        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', 'selected: '+x))

class CustomButtonDemoScreen(CustomScreen):
    pass

    def show_popup(self):
        print 'show popup...'
        #App.get_running_app().navigation_popup.open()
        # App.get_running_app()._screenmanager.open_all_screens()
        App.get_running_app()._screenmanager.get_all_thumbnails(self._show_it)

        #App.get_running_app().raise_error('A', 'B')

    @mainthread
    def _show_it(self):
        App.get_running_app()._screenmanager.show_navigation_popup()


class CustomCheckBoxDemoScreen(CustomScreen):
    pass

class CustomSliderDemoScreen(CustomScreen):
    pass

class CustomLayoutsScreen(CustomScreen):
    def __init__(self, *largs, **kwargs):
        super(CustomLayoutsScreen, self).__init__(*largs, **kwargs)

        gl = GroupedLayout()
        gl.title = 'Grouped Layout'
        gl.theme = ('app', 'grouped_layout')
        # gl.width = dp(200)

        btn = Button(text='test?', size_hint=(None,None), size=(dp(120), dp(50)))
        gl.add_widget(btn)

        btn = Button(text='testB', size_hint_y=None, height=dp(50))
        btn.size_hint_x = None
        btn.width = dp(200)
        btn.background_color = (.1, .4, .2, 1.0)
        gl.add_widget(btn)

        btn = Button(text='testC', size_hint_y=None, height=dp(50))
        btn.size_hint_x = None
        btn.width = dp(200)
        btn.background_color = (.1, .4, .2, 1.0)
        gl.add_widget(btn)

        self.add_widget(gl)


class DropShadowScreen(CustomScreen):
    def __init__(self, *largs, **kwargs):
        super(DropShadowScreen, self).__init__(*largs, **kwargs)

        label = Label(text='Label with default shadow',
                     size_hint=(None,None), size=(dp(200), dp(40)), color=(0,0,0,1),
                    )
        with label.canvas.before:
            Color(.85,.85, .7, 1)
            label.rect = Rectangle(size=label.size, pos=label.pos)

        label.bind(size=self._update_rect, pos=self._update_rect)

        ds = DropShadow(label, height_offset=5)
        ds.blur_radius = 4
        ds.offset = 4
        self.add_widget(ds)


        btn = Button(text='Button with colored shadow', size_hint=(None,None), size=(dp(250), dp(50)))
        ds = DropShadow(btn, height_offset=15)
        ds.blur_radius = 3
        ds.shadow_color = (0.1, 0.5, 0.1, 0.8)
        self.add_widget(ds)
        btn.bind(on_release=lambda instance: setattr(ds, 'offset', 5))
        btn.bind(on_press=lambda instance: setattr(ds, 'offset', 2))


        btn = CustomButton(text='CustomButton with matching\nshadow radius', size_hint=(None,None), size=(dp(250), dp(50)))
        btn.theme = ('app', 'default')
        btn.radius = dp(20)
        ds2 = DropShadow(btn)
        ds2.radius = 20
        ds2.offset = 10
        ds2.blur_radius = 10
        ds2.shadow_color = (0.5, 0.1, 0.5, 0.5)
        self.add_widget(ds2)
        btn.bind(on_release=lambda instance: setattr(ds2, 'offset', 10))
        btn.bind(on_press=lambda instance: setattr(ds2, 'offset', 3))


        label = Label(text='StyledLayout with default shadow',
                     size_hint_y=None, height=dp(30), color=(0,0,0,1),
                    )
        self.add_widget(label)

        self.layout = StyledLayout()
        self.layout.size = (dp(250), dp(200))
        self.layout.radius = 5

        label = Label(text='Press the buttons to change \nsimulated height',
                     size_hint_y=None, height=dp(50), color=(0,0,0,1),
                    )
        self.layout.add_widget(label)

        btn = Button(text='High', size_hint_y=None, height=dp(50))
        self.layout.add_widget(btn)
        btn.bind(on_release=self._layout_btn_released)
        btn.bind(on_press=self._btn_high_pressed)

        btn = Button(text='Med', size_hint_y=None, height=dp(50))
        self.layout.add_widget(btn)
        btn.bind(on_release=self._layout_btn_released)
        btn.bind(on_press=self._btn_med_pressed)

        btn = Button(text='Low', size_hint_y=None, height=dp(50))
        self.layout.add_widget(btn)
        btn.bind(on_release=self._layout_btn_released)
        btn.bind(on_press=self._btn_low_pressed)

        self.ds2 = DropShadow(self.layout)
        self.ds2.blur_radius = 8
        self.ds2.offset = 16
        self.ds2.radius = self.layout.radius

        self.add_widget(self.ds2)

        # TODO: fix the issue w/ the shadow widget height not getting
        #       corrected when the widget height changes
        # self.layout.height = dp(200)


    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


    def _btn_high_pressed(self, instance):
        self.ds2.offset = 9
        self.ds2.blur_radius = 6

    def _btn_med_pressed(self, instance):
        self.ds2.offset = 6
        self.ds2.blur_radius = 4

    def _btn_low_pressed(self, instance):
        self.ds2.offset = 3
        self.ds2.blur_radius = 2

    def _layout_btn_released(self, instance):
        self.ds2.offset = 16
        self.ds2.blur_radius = 12


class CustomGraphScreen(Screen):

    def __init__(self, *largs, **kwargs):
        super(CustomGraphScreen, self).__init__(*largs, **kwargs)

        b = BoxLayout(orientation='vertical')
        b.size_hint_y = None
        b.height = dp(250)

        # example of a custom theme
        colors = itertools.cycle([
            rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])
        graph_theme = {
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            'background_color': rgb('f8f8f2'),  # back ground color of canvas
            'tick_color': rgb('808080'),  # ticks and grid
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
            **graph_theme)

        graph._with_stencilbuffer = False
        #graph.size_hint_y = None
        #graph.height = dp(250)
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

        # plot = BarPlot(color=next(colors), bar_spacing=.72)
        # graph.add_plot(plot)
        # plot.bind_to_graph(graph)
        # plot.points = [(x, .1 + randrange(10) / 10.) for x in range(-50, 1)]

        Clock.schedule_interval(self.update_points, 1 / 10.)

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
            **graph_theme)

        b.add_widget(graph)
        graph2._with_stencilbuffer = False
        #graph2.size_hint_y = None
        #graph2.height = dp(250)

        if np is not None:
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

            b.add_widget(graph2)
            self.contourplot = plot

            Clock.schedule_interval(self.update_contour, 1 / 10.)

        self.add_widget(b)

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



