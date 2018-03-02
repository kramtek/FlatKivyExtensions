

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

from flat_kivy_extensions.uix.customscreen import CustomScreen

from flat_kivy_extensions.uix.customlayouts import StyledLayout, GroupedLayout
from flat_kivy_extensions.uix.dropshadow import DropShadow

Builder.load_string('''
<-CustomScreen1>:
    title: 'A Custom Screen'
    theme: ('app', 'screen')

    Label:
        text: 'Widgets in custom screen in StackLayout'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

    Button:
        text: 'button'
        size_hint: None, None
        size: '130dp', '60dp'

    Label:
        text: 'Label'
        size_hint: None, None
        size: dp(200), dp(50)
        color: (0,0,0,1)

<-CustomScreen2>:
    title: 'CS #2'
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

<-CustomScreen3>:
    title: 'Another Custom Screen'
    theme: ('app', 'screen')

<-CustomScreen4>:
    title: 'Custom #3'
    theme: ('app', 'screen')

    # Button:
    #     text: 'button'
    #     size_hint_y: None
    #     height: '50dp'
    #
    # DropShadow:
    #     blur_rad: 2
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)
    #
    # DropShadow:
    #     blur_rad: 4
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)
    #
    # DropShadow:
    #     blur_rad: 8
    #     offset_scaling: 0.5
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)
    #
    # DropShadow:
    #     blur_rad: 8
    #
    #     StyledLayout:
    #         size: dp(150), dp(70)

''')


class CustomScreen1(CustomScreen):
    pass

class CustomScreen2(CustomScreen):
    pass

class CustomScreen3(CustomScreen):
    def __init__(self, *largs, **kwargs):
        super(CustomScreen3, self).__init__(*largs, **kwargs)

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


class CustomScreen4(CustomScreen):
    def __init__(self, *largs, **kwargs):
        super(CustomScreen4, self).__init__(*largs, **kwargs)

        btn = Button(text='test', size_hint=(None,None), size=(dp(100), dp(50)))
        self.ds1 = DropShadow(btn)
        self.ds1.blur_rad = 4
        self.ds1.offset = 4
        self.ds1.radius = 0
        self.ds1.shadow_color = (0.1, 0.5, 0.1, 0.8)
        self.add_widget(self.ds1)

        btn = Button(text='test', size_hint_y=None, height=dp(50))
        self.add_widget(btn)
        btn.bind(on_release=self._btn_released)
        btn.bind(on_press=self._btn_pressed)

        self.myWidget = StyledLayout()
        self.myWidget.size = (dp(250), dp(200))

        btn = Button(text='test2', size_hint_y=None, height=dp(50))
        self.myWidget.add_widget(btn)
        btn = Button(text='test3', size_hint_y=None, height=dp(50), size_hint_x=None, width=dp(150))
        self.myWidget.add_widget(btn)
        btn = Button(text='test4', size_hint_y=None, height=dp(100))
        self.myWidget.add_widget(btn)

        self.ds2 = DropShadow(self.myWidget)
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



