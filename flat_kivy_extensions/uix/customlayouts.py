

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout

from flat_kivy.uix.flatlabel import FlatLabel

Builder.load_string('''

<-StyledLayout>:
    orientation: 'tb-lr'
    size_hint: 1, None
    
    background_color: (0.0, 0.5, 0.5, 1.0)
    border_line_width: 2.0
    border_color: (.1, .1, .1, 0.0)
    radius: 10
    
    padding: '5dp'
        
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [dp(self.radius),dp(self.radius),dp(self.radius),dp(self.radius)]
        Color:
            rgba: self.border_color
        Line
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(self.radius)]
            width: dp(self.border_line_width)

    FlatButton:
        text: 'button 1'
        theme: ('green', 'accent')
        size_hint_y: None
        height: '50dp'
        size_hint_x: None
        width: '145dp'

<_WidgetContainerLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (1.0, 0.5, 1.0, 1.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos
    
<_MainLayout>:
    canvas.before:
        Color:
            rgba: (0.95, 0.95, 0.0, 1.0)
        Rectangle:
            size: self.size
            pos: self.pos
            
<_ContentLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (0.4, 0.2, 0.1, 1.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

''')

class _WidgetContainerLayout(BoxLayout):
    ''' Dummy layout to wrap a widget of fixed size and ensure that
    the widget is centerd horizontally.  Since it is assumed that
    All widgets added to a CustomScreen are fixed height then the
    container layout holding the widget is forced to have the same height
    '''
    pass

class _MainLayout(BoxLayout):
    pass


class _ContentLayout(GridLayout):
    pass

class StyledLayout(StackLayout):

    min_height_required = NumericProperty(5)

    def __init__(self, *largs, **kwargs):
        self._forward_call = None
        super(StyledLayout, self).__init__(*largs, **kwargs)
        print 'type of ???: %s' % str(self.min_height_required)

    def _calculate_minimum_height(self, *largs, **kwargs):
        print('largs: %s' % str(largs))
        self.mx = 0
        mn = 2*self.padding[0]
        for child in self.children:
            mn += child.height + self.spacing[0]
            if child.width > self.mx:
                self.mx = child.width
        print 'a: %s        mx: %s' % (str(self.min_height_required), str(self.mx))
        print type(self.min_height_required)
        self.min_height_required = mn
        # print 'type of ???: %s' % str(type(self.min_height_required))
        # raw_input()
        print '- adjusted minimum height required for layout: %f' % float(self.min_height_required)
        # return self.min_height_required

        self.height = self.min_height_required
        # self.width = self.mx

    def _center(self, instance, value):
        if instance.parent is not None:
            if isinstance(instance.parent, _WidgetContainerLayout):
                instance.center_x = instance.parent.center_x

    def add_widget(self, *largs, **kwargs):
        # super(StyledLayout, self).add_widget(*largs, **kwargs)

        widget = largs[0];

        container = _WidgetContainerLayout()
        container.size_hint_y = None
        widget.container = container
        widget.bind(height=container.setter('height'))
        container.height = widget.height
        widget.bind(pos=self._center)
        container.add_widget(widget)
        print 'adding widget: %s' % str(widget)
        super(StyledLayout, self).add_widget(container)
        self._calculate_minimum_height()

        widget.bind(height=self._calculate_minimum_height)
        widget.bind(width=self._calculate_minimum_height)

    def remove_widget(self, widget):
        # super(StyledLayout, self).remove_widget(widget)
        container = widget.container
        container.remove_widget(widget)
        super(StyledLayout, self).remove_widget(container)
        minimum_height_required = self._calculate_minimum_height()
        self.height = self.min_height_required
        print 'removed widget: minimum height required for layout: %f' % float(self.min_height_required)

    def _set_forward_call(self, callback):
        self._forward_call = callback

    def on_min_height_required(self, instance, value):
        print 'on min height required, forward call: %s' % str(self._forward_call)
        if self._forward_call is not None:
            self._forward_call(instance, value)


class GroupedLayout(StyledLayout):
    pass
    # title = StringProperty('SomeScreen')
    # theme = ListProperty()
    # style = StringProperty()
    # # min_height = NumericProperty(0)
    #
    # def __init__(self, *largs, **kwargs):
    #
    #     self._content_layout = _ContentLayout(orientation='vertical', cols=1,
    #                                         padding=dp(5), spacing=dp(3),
    #                                         )
    #     self._content_layout.size_hint_y = None
    #     self._content_layout.width = dp(200)
    #
    #     super(GroupedLayout, self).__init__(*largs, **kwargs)
    #     self._forward_call = self._resize
    #
    #     print 'forward call: %s' % str(self._forward_call)
    #
    #     # self._main_layout = _MainLayout(orientation='vertical',
    #     #                               padding=dp(2), spacing=dp(2),
    #     #                               )
    #     # self._main_layout.size_hint_y = None
    #
    #     self._title_label = FlatLabel(text=self.title,
    #                                 theme=self.theme,
    #                                 )
    #     self.bind(title=self._title_label.setter('text'))
    #
    #     # Question: can style be set in constructor, or does
    #     # property propagation require setting style after theme?
    #     self.bind(theme=self._title_label.setter('theme'))
    #     # self.bind(style=self._title_label.setter('style'))
    #     # self._main_layout.add_widget(self._title_label)
    #     super(GroupedLayout, self).add_widget(self._title_label)
    #
    #     # self._main_layout.add_widget(self._content_layout)
    #     super(GroupedLayout, self).add_widget(self._content_layout)
    #
    #     # super(GroupedLayout, self).__init__(*largs, **kwargs)
    #
    #     # super(GroupedLayout, self).add_widget(self._main_layout)
    #
    #     # self._content_layout.bind(size=self._update_content_layout)
    #
    #     # super(GroupedLayout, self).bind(min_height_required = self._resize)
    #
    #     print 'forward call: %s' % str(self._forward_call)
    #
    #     # self.bind(min_height_required=self._content_layout.setter('height'))
    #
    #     self._content_layout.size_hint = (None, None)
    #     self._content_layout.height = self.height + dp(60)
    #     self._content_layout.width = dp(200)
    #
    # def _resize(self, instance, value):
    #     print 'minium height %s changed for: %s' % (str(self.min_height_required), str(instance))
    #
    #     temp = getattr(self, 'min_height_required')
    #     print 'temp: %s' % str(temp)
    #     # self._content_layout.height = float(temp)
    #
    #     pass
    #
    # def on_height(self, instance, height):
    #     print 'adjusting height of group layout'
    #     # self._content_layout.height = height
    #     # self._content_layout.width = dp(200)
    #
    # def on_size(self, instance, size):
    #     print 'sizing group layout to: %s' % str(size)
    #     # self._content_layout.height = size[1]
    #     # self._content_layout.width = dp(200)
    #
    # def _center(self, instance, value):
    #     if instance.parent is not None:
    #         if isinstance(instance.parent, _WidgetContainerLayout):
    #             instance.center_x = instance.parent.center_x
    #
    # def add_widget(self, widget):
    #     # Put each widget into a box layout so that  whatever is actually added
    #     # to GridLayout does not have a fixed width
    #     container = _WidgetContainerLayout()
    #     container.size_hint_y = None
    #     widget.bind(height=container.setter('height'))
    #     container.height = widget.height
    #     widget.bind(pos=self._center)
    #     container.add_widget(widget)
    #     self._content_layout.add_widget(container)
    #
    #
    # def remove_widget(self, widget):
    #     widget.container.remove_widget(widget)
    #     self._content_layout.remove_widget(widget.container)
    #     self._content_layout.height = self.min_height_required

