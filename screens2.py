

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.metrics import dp

from flat_kivy_extensions.uix.customscreen import CustomScreen

Builder.load_string('''
#: import ew kivy.uix.effectwidget
<-CustomScreen1>:
    title: 'Custom #1'
    theme: ('app', 'screen')
    style: 'HeaderTitle'

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
                offset_y: 10 - root.offset
                offset_x: root.offset
                additional_offset_y: 10
                offset_y: 10.0-root.offset + self.additional_offset_y
                
                canvas.before:
                    Color:
                        rgba: root.shadow_color
                    RoundedRectangle:
                        size: self.size
                        pos: (self.pos[0] + dp(self.offset_x), self.pos[1] + dp(self.offset_y))
                        radius: [dp(root.radius),dp(root.radius),dp(root.radius),dp(root.radius)]

                on_parent: root._add_widget_to_shadow()

    # SomeLayout:
    #     size: root.widget_size


<-SomeLayout>:
    orientation: 'tb-lr'
    size_hint: None, None

    padding: '5dp'

    radius: 10
    
    canvas.before:
        Color:
            rgba: (0.0, 0.5, 0.5, 1.0)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [dp(self.radius),dp(self.radius),dp(self.radius),dp(self.radius)]
        Color:
            rgba: (.1, .1, .1, 1.0)
        Line
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(self.radius)]
            width: dp(1)

    FlatButton:
        text: 'button'
        theme: ('green', 'accent')
        size_hint_y: None
        height: '50dp'

''')


class DropShadowLayout(AnchorLayout):
    def __init__(self, widget, *largs, **kwargs):
        self.widget = widget
        super(DropShadowLayout, self).__init__(*largs, **kwargs)

    def _add_widget_to_shadow(self):
        self.widget.bind(size=self._resize)
        self._resize(self.widget, None)
        self.add_widget(self.widget)

    def _resize(self, instance, value):
        self.size = (instance.width, instance.height+dp(20))
        self.container_size = (instance.width + dp(20), instance.height + dp(20))
        self.widget_size = instance.size

class SomeLayout(StackLayout):
    pass

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

        myWidget = SomeLayout()
        myWidget.size = (dp(300), dp(200))
        self.ds2 = DropShadowLayout(myWidget)
        self.ds2.blur_rad = 8
        self.ds2.offset = 12
        self.ds2.radius = 10

        # myWidget.height = dp(101)

        self.add_widget(self.ds2)

    def _btn_pressed(self, instance):
        # Question: can the offset and blur_rad properties
        #           be combined such that they are updated
        #           at the same time rather than sequentially
        self.ds2.offset = 6
        self.ds2.blur_rad = 4

        self.ds1.offset = 1
        print 's: %s' % str(self.ds1.widget_size)

    def _btn_released(self, instance):
        self.ds2.blur_rad = 8
        self.ds2.offset = 12

        self.ds1.offset = 4



