

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

from flat_kivy_extensions.uix.customscreen import CustomScreen

Builder.load_string('''
#: import ew kivy.uix.effectwidget
<-CustomScreen1>:
    title: 'Custom #1'
    theme: ('app', 'screen')

    # Button:
    #     text: 'button'
    #     size_hint_y: None
    #     height: '50dp'
    # 
    # DropShadowLayout:
    #     blur_rad: 2
    #     
    #     SomeLayout:
    #         size: dp(150), dp(70)
    # 
    # DropShadowLayout:
    #     blur_rad: 4
    #     
    #     SomeLayout:
    #         size: dp(150), dp(70)
    # 
    # DropShadowLayout:
    #     blur_rad: 8
    #     offset_scaling: 0.5
    # 
    #     SomeLayout:
    #         size: dp(150), dp(70)
    #         
    # DropShadowLayout:
    #     blur_rad: 8
    # 
    #     SomeLayout:
    #         size: dp(150), dp(70)


<-DropShadowLayout>:
    blur_rad: 8.0
    offset: 5
    background_color: (1.0, 1.0, 1.0, 1.0)
    shadow_color: (0.1, 0.1, 0.1, 0.6)
    
    radius: 0
    
    size_hint: None, None
    size: dp(10), dp(15)
    widget_size: dp(10), dp(10)
    container_size: dp(15), dp(15)
    overhead: dp(15)

    anchor_x: 'left'
    anchor_y: 'top'

    BoxLayout:
        orientation: 'vertical' 
        size_hint: None, None
        size: root.container_size

        canvas.before:
            Color:
                rgba: (.1, .2, .3, 1)
            Rectangle:
                size: self.size
                pos: self.pos
                
        EffectWidget:

            blur_rad: root.blur_rad

            effects: ew.VerticalBlurEffect(size=dp(self.blur_rad)), ew.HorizontalBlurEffect(size=dp(self.blur_rad))
            background_color: root.background_color
            size_hint: None, None
            size: root.container_size

            canvas.before:
                Color:
                    rgba: (.1, .2, .3, 1.0)
                Rectangle:
                    size: self.size
                    pos: self.pos
                
            BoxLayout:
                size_hint: None, None
                size: root.widget_size
                offset_x: root.offset
                offset_y: root.overhead-root.offset
                
                canvas.before:
                    Color:
                        rgba: root.shadow_color
                    RoundedRectangle:
                        size: self.size
                        pos: (self.pos[0] + dp(self.offset_x), self.pos[1] + dp(self.offset_y))
                        radius: [dp(root.radius),dp(root.radius),dp(root.radius),dp(root.radius)]

                on_parent: root._add_widget_to_shadow()


<-SomeLayout>:
    orientation: 'tb-lr'
    size_hint: None, None
    
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

<_WidgetContainerLayout>:
    # canvas.before:
    #     Color:
    #         rgba: (1.0, 0.5, 1.0, 1.0)
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

class DropShadowLayout(AnchorLayout):
    def __init__(self, widget, *largs, **kwargs):
        self.widget = widget
        super(DropShadowLayout, self).__init__(*largs, **kwargs)

    def _add_widget_to_shadow(self):
        self.widget.bind(size=self._resize)
        self._resize(self.widget, None)
        self.add_widget(self.widget)

    def _resize(self, instance, value):
        self.size = (instance.width, instance.height+dp(25))
        overhead = 20
        self.container_size = (instance.width + dp(overhead), instance.height + dp(overhead))
        self.overhead = overhead
        self.widget_size = instance.size


class SomeLayout(StackLayout):

    def __init__(self, *largs, **kwargs):
        super(SomeLayout, self).__init__(*largs, **kwargs)

    def _calculate_minimum_height(self):
        min_height = 2*self.padding[0]
        for child in self.children:
            min_height += child.height + self.spacing[0]
        return min_height

    def _center(self, instance, value):
        if instance.parent is not None:
            if isinstance(instance.parent, _WidgetContainerLayout):
                instance.center_x = instance.parent.center_x

    def add_widget(self, *largs, **kwargs):
        # super(SomeLayout, self).add_widget(*largs, **kwargs)

        widget = largs[0];

        container = _WidgetContainerLayout()
        container.size_hint_y = None
        widget.container = container
        widget.bind(height=container.setter('height'))
        container.height = widget.height
        widget.bind(pos=self._center)
        container.add_widget(widget)
        super(SomeLayout, self).add_widget(container)

        minimum_height_required = self._calculate_minimum_height()
        self.height = minimum_height_required
        print 'added widget: minimum height required for layout: %f' % float(minimum_height_required)

    def remove_widget(self, widget):
        # super(SomeLayout, self).remove_widget(widget)
        container = widget.container
        container.remove_widget(widget)
        super(SomeLayout, self).remove_widget(container)
        minimum_height_required = self._calculate_minimum_height()
        self.height = minimum_height_required
        print 'removed widget: minimum height required for layout: %f' % float(minimum_height_required)



class CustomScreen1(CustomScreen):
    def __init__(self, *largs, **kwargs):
        super(CustomScreen1, self).__init__(*largs, **kwargs)

        btn = Button(text='test', size_hint=(None,None), size=(dp(100), dp(50)))
        self.ds1 = DropShadowLayout(btn)
        self.ds1.blur_rad = 4
        self.ds1.offset = 4
        self.ds1.radius = 0
        self.ds1.shadow_color = (0.1, 0.5, 0.1, 0.8)
        self.add_widget(self.ds1)

        btn = Button(text='test', size_hint_y=None, height=dp(50))
        self.add_widget(btn)
        btn.bind(on_release=self._btn_released)
        btn.bind(on_press=self._btn_pressed)

        self.myWidget = SomeLayout()
        self.myWidget.size = (dp(250), dp(200))

        btn = Button(text='test2', size_hint_y=None, height=dp(50))
        self.myWidget.add_widget(btn)
        btn = Button(text='test3', size_hint_y=None, height=dp(50), size_hint_x=None, width=dp(150))
        self.myWidget.add_widget(btn)
        btn = Button(text='test4', size_hint_y=None, height=dp(100))
        self.myWidget.add_widget(btn)

        self.ds2 = DropShadowLayout(self.myWidget)
        self.ds2.blur_rad = 8
        self.ds2.offset = 12
        self.ds2.radius = 10

        self.add_widget(self.ds2)

        # TODO: fix the issue w/ the shadow widget height not getting
        #       corrected when the widget height changes
        # self.myWidget.height = dp(200)

    def _btn_pressed(self, instance):
        # Question: can the offset and blur_rad properties
        #           be combined such that they are updated
        #           at the same time rather than sequentially
        self.ds2.offset = 6
        self.ds2.blur_rad = 4

        self.ds1.offset = 1

    def _btn_released(self, instance):
        self.ds2.blur_rad = 8
        self.ds2.offset = 12

        self.ds1.offset = 4



