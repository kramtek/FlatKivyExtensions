
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.properties import StringProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Fbo, Scale, Translate, Color

from flat_kivy.uix.flatlabel import FlatLabel
from flat_kivy.uix.flatbutton import FlatButton

from flat_kivy_extensions.uix.dropshadow import DropShadow

from flat_kivy_extensions.uix.thumbnailwidget import ThumbNailWidget

#_ContentLayout = BoxLayout
# _ContentLayout = GridLayout

Builder.load_string('''
<_WidgetContainerLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (1.0, 0.5, 1.0, 1.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

<_ContentLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (0.95, 0.95, 0.95, 1.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

<_MainLayout>:
    border_color: (.1, .1, .3, 1.0)
    border_line_width: 0.5
    radius: 2

    canvas.before:
        Color:
            rgba: (0.95, 0.95, 0.95, 1.0)
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: self.border_color
        Line
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(self.radius)]
            width: dp(self.border_line_width)

<_OuterLayout>:
    canvas.before:
        Color:
            rgba: (0.95, 0.95, 0.95, 1.0)
        Rectangle:
            size: self.size
            pos: self.pos

''')

class _WidgetContainerLayout(BoxLayout):
    ''' Dummy layout to wrap a widget of fixed size and ensure that
    the widget is centerd horizontally.  Since it is assumed that
    All widgets added to a CustomScreen are fixed height then the
    container layout holding the widget is forced to have the same height
    '''
    pass

class _ContentLayout(GridLayout):
    pass

class _MainLayout(BoxLayout):
    pass

class _OuterLayout(BoxLayout):
    pass

class CustomScreen(Screen):
    title = StringProperty('SomeScreen')
    theme = ListProperty()
    style = StringProperty()

    def __init__(self, *largs, **kwargs):
        self._main_layout = _MainLayout(orientation='vertical',
                                      padding=dp(2), spacing=dp(2),
                                      )
        self._title_label = FlatLabel(text=self.title,
                                    theme=self.theme,
                                    )
        self.bind(title=self._title_label.setter('text'))
        # Question: can style be set in constructor, or does
        # property propagation require setting style after theme?
        self.bind(theme=self._title_label.setter('theme'))
        # self.bind(style=self._title_label.setter('style'))
        self._main_layout.add_widget(self._title_label)

        self._content_layout = _ContentLayout(orientation='vertical', cols=1,
                                            padding=dp(5), spacing=dp(3),
                                            )
        self._main_layout.add_widget(self._content_layout)

        super(CustomScreen, self).__init__(*largs, **kwargs)

        self.outer_container = _OuterLayout()

        padding = 5
        height_offset = 4
        header_height = 40
        #blur_radius = 4
        #shadow_offset = 6
        #shadow_color = (0.3, 0.1, 0.1, 0.5)

        self.container_height = Window.height - dp(header_height) - dp(2*padding) - dp(height_offset) - self._title_label.height - 2*dp(padding) - 2*self._main_layout.padding[0]
        if True:
            self.outer_container.add_widget(self._main_layout)
            super(CustomScreen, self).add_widget(self.outer_container)
            #super(CustomScreen, self).add_widget(self._main_layout)
            return

        padding = 5
        height_offset = 4
        header_height = 40
        blur_radius = 4
        shadow_offset = 6
        shadow_color = (0.3, 0.1, 0.1, 0.5)

        self.outer_container.padding = dp(padding)
        self._main_layout.size_hint = (None, None)
        self._main_layout.height = Window.height - dp(header_height) - dp(2*padding) - dp(height_offset)
        self._main_layout.width = Window.width - dp(2*padding+height_offset)
        self.outer_container.add_widget(self._main_layout)
#        ds = DropShadow(self._main_layout, height_offset=height_offset)
#        ds.blur_radius = blur_radius
#        ds.offset = shadow_offset
#        ds.shadow_color = shadow_color
#        self.outer_container.add_widget(ds)

        #self.container_height = Window.height - dp(header_height) - dp(2*padding) - dp(height_offset) - self._title_label.height - 2*dp(padding) - 2*self._main_layout.padding[0]

        super(CustomScreen, self).add_widget(self.outer_container)

    def on_size(self, instance, value):
        # Experiment with reorganizing children based on screen orientation
        if value[0] > value[1]:
            self._content_layout.cols = 2
        else:
            self._content_layout.cols = 1

    def _center(self, instance, value):
        if instance.parent is not None:
            if isinstance(instance.parent, _WidgetContainerLayout):
                instance.center_x = instance.parent.center_x

    def add_widget(self, widget):
        # Put each widget into a box layout so that  whatever is actually added
        # to GridLayout does not have a fixed width
        container = _WidgetContainerLayout()
        container.size_hint_y = None
        widget.bind(height=container.setter('height'))
        container.height = widget.height
        widget.bind(pos=self._center)
        container.add_widget(widget)
        self._content_layout.add_widget(container)

    def remove_widget(self, widget):
        widget.container.remove_widget(widget)
        self._content_layout.remove_widget(widget.container)

