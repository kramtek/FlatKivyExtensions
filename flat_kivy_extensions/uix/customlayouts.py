
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout

from flat_kivy.uix.flatlabel import FlatLabel

from flat_kivy_extensions.uix.customcheckbox import CustomCheckBoxListItem

from flat_kivy_extensions import PackageLogger
log = PackageLogger(__name__, moduleDebug=False)

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

<_WidgetContainerLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (1.0, 0.5, 1.0, 1.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

<_MainLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (0.95, 0.95, 0.0, 1.0)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

<_ContentLayout>:
    height: self.minimum_height
    cols: 1
    # canvas.before:
    #     Color:
    #         rgba: (0.4, 0.2, 0.1, 0.5)
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

<-ChoiceLayout>:
    orientation: 'vertical'
    size_hint: None, None
    size: (dp(200), dp(0))

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


class ChoiceLayout(BoxLayout):

    theme = ObjectProperty(('', ''))
    selected = ObjectProperty(None, allownone=True)
    exclusive = BooleanProperty(False)
    disabled = BooleanProperty(False)

    def __init__(self, *largs, **kwargs):
        if 'exclusive' in kwargs.keys():
            self.exclusive = kwargs['exclusive']
            del(kwargs['exclusive'])
        super(ChoiceLayout, self).__init__(*largs, **kwargs)
        self._currentChoice = None

    def on_disabled(self, instance, value):
        for child in self.children:
            child.disabled = value

    def selectChoice(self, instance, value):
        if value:
            self._currentChoice = instance.text
            self.selected = instance.text

    def setup(self, labels, detail_text=None):
        for index, label in enumerate(labels):
            #item = ChoiceListItem(text=label)
            item = CustomCheckBoxListItem(text=label)
            item.theme = self.theme
            if detail_text is not None:
                item.detail_text = detail_text[index]
                item.detail_font_size = dp(10)
            if self.exclusive:
                item.group = str(id(self))
            item.exclusive = True
            item.height = dp(45)
            item.bind(active=self.selectChoice)
            self.bind(theme=item.setter('theme'))
            self.add_widget(item)

            if self.exclusive:
                item.icon = 'fa-circle'
                item.radius = item.height * 0.25
                item.check_scale = 0.45 * item.size_scaling
            else:
                item.size_scaling = 0.5
                item.check_scale = .35

        self.height = dp(45)*len(labels)






class StyledLayout(StackLayout):

    _min_height_required = NumericProperty(5)

    def __init__(self, *largs, **kwargs):
        self._forward_call = None
        super(StyledLayout, self).__init__(*largs, **kwargs)

    def _calculate_minimum_height(self, *largs, **kwargs):
        mn = 2*self.padding[0]
        for child in self.children:
            mn += child.height + self.spacing[0]
        self._min_height_required = mn
        self.height = self._min_height_required

    def _center(self, instance, value):
        if instance.parent is not None:
            if isinstance(instance.parent, _WidgetContainerLayout):
                instance.center_x = instance.parent.center_x

    def add_widget(self, widget, **kwargs):
        ''' Overriden method to have widget added to content container layout
        rather than directly to this (Stack) Layout
        '''
        container = _WidgetContainerLayout()
        container.size_hint_y = None
        widget.container = container
        widget.bind(height=container.setter('height'))
        container.height = widget.height
        widget.bind(pos=self._center)
        container.add_widget(widget)

        super(StyledLayout, self).add_widget(container, **kwargs)
        self._calculate_minimum_height()

        widget.bind(height=self._calculate_minimum_height)
        widget.bind(width=self._calculate_minimum_height)

    def remove_widget(self, widget):
        ''' Overriden method to have widget removed from content container layout
        rather than directly from this (Stack) Layout
        '''
        container = widget.container
        container.remove_widget(widget)
        super(StyledLayout, self).remove_widget(container)
        self._calculate_minimum_height()
        self.height = self._min_height_required


class GroupedLayout(StyledLayout):
    title = StringProperty('SomeScreen')
    ''' String used for the layout title
    '''
    theme = ListProperty()
    ''' Theme applied to the layout title.
    '''
    style = StringProperty()
    ''' Font style applied to the layout title.
    '''

    def __init__(self, *largs, **kwargs):

        self._content_layout = _ContentLayout(orientation='tb-lr', size_hint_y=None,
                                            padding=dp(5), spacing=dp(5),
                                            )

        super(GroupedLayout, self).__init__(*largs, **kwargs)

        self._title_label = FlatLabel(text=self.title,
                                    theme=self.theme,
                                    )
        self.bind(title=self._title_label.setter('text'))

        self.bind(theme=self._title_label.setter('theme'))

        super(GroupedLayout, self).add_widget(self._title_label)

        super(GroupedLayout, self).add_widget(self._content_layout)

        self._content_layout.size_hint = (None, None)

        self.bind(width=self._content_layout.setter('width'))

    def _center(self, instance, value):
        if instance.parent is not None:
            if isinstance(instance.parent, _WidgetContainerLayout):
                instance.center_x = instance.parent.center_x

#    def _calc_height(self):
#        ht = self._content_layout.padding[0]*2
#        for child in self._content_layout.children:
#            ht += child.height
#        if len(self._content_layout.children) > 1:
#            ht += (len(self._content_layout.children)-1)*self._content_layout.spacing[0]
#        return ht

    def add_widget(self, widget, *kwargs):
        ''' Overriden method to have widget added to content container layout
        rather than directly to this (Stack) Layout
        '''
        container = _WidgetContainerLayout()
        # Put each widget into a box layout so that  whatever is actually added
        # to GridLayout does not have a fixed width
        container = _WidgetContainerLayout()
        container.size_hint_y = None
        widget.bind(height=container.setter('height'))
        container.height = widget.height
        widget.bind(pos=self._center)
        container.add_widget(widget, *kwargs)
        self._content_layout.add_widget(container)
#        ht = self._calc_height();
#        self._content_layout.height = ht

    def remove_widget(self, widget):
        ''' Overriden method to have widget removed from content container layout
        rather than directly from this (Stack) Layout
        '''
        container = widget.container
        widget.container.remove_widget(widget)
        self._content_layout.remove_widget(widget.container)
#        ht = self._calc_height();
#        self._content_layout.height = ht

