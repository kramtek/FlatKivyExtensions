

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

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
        check_color_hue_down: '8#00'
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
        check_scale: .5
        on_active: if self.active: print('warning activated')
        current_state: True

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
        height: '60dp'

    CustomSlider:
        orientation: 'vertical'
        min: 10
        max: 110
        theme: ('green', 'main')
        height: '120dp'

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

''')


class KivyWidgetScreen(CustomScreen):
    pass

class CustomButtonDemoScreen(CustomScreen):
    pass

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


