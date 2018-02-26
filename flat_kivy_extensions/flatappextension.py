
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, FadeTransition, NoTransition

from flat_kivy.flatapp import FlatApp
from flat_kivy.uix.flattextinput import FlatTextInput
from flat_kivy.uix.flaticonbutton import FlatIconButtonLeft
from flat_kivy.uix.flatlabel import FlatLabel

from flat_kivy_extensions.uix.customiconbutton import CustomIconButton

Builder.load_string('''
#:import NavigationDrawer kivy_garden.navigationdrawer.NavigationDrawer
#:import NoTransition kivy.uix.screenmanager.NoTransition
<RootWidget>:
    title: 'Some App Title'
    background_color: 1.0, 1.0, 1.0
    header_height: dp(40)
    header_color: 0.1, 0.1, 0.2
    side_panel_color: 0.1, 0.1, 0.1


    BoxLayout:
        id: main_layout
        orientation: 'vertical'
        size_hint: (None, None)
        size: root.size
        canvas.before:
            Color:
                rgba: root.background_color
            Rectangle:
                pos: self.pos
                size: self.size

        HeaderLayout:
            id: header
            size_hint_y: None
            height: root.header_height
            title: root.title
            color: root.header_color

        NavigationDrawer:
            id: navigationdrawer
            height: root.height
            width: root.width
            side_panel_width: min(dp(250), 0.6*self.width)
            anim_type:  'slide_above_simple'

            BoxLayout:
                id: side_panel
                orientation: 'vertical'

                # this will be populated dynamically when app starts

            BoxLayout:
                id: screencontent
                orientation: 'vertical'

                ScreenManager:
                    id: screenmanager
                    transition: NoTransition()
                    #transition: FadeTransition()
                    #transition: FadeTransition()
                    canvas.before:
                        Color:
                            rgb: root.background_color
                        Rectangle:
                            pos: self.pos
                            size: self.size

<-HeaderLayout>:
    header_height: '40dp'
    title: 'Header'
    color: .1, .9, .1
    canvas.before:
        Color:
            rgb: root.color
        Rectangle:
            pos: self.pos
            size: self.size

    CustomIconButton:
        id: _menu_button
        theme: ('app', 'header')
        icon: 'fa-bars'
        size_hint_x: None
        width: root.header_height
        icon_font_size: dp(30)

    FlatLabel:
        id: title_label
        text: root.title
        color_tuple: ('Gray', '000')
        style: 'Subhead'


<-SomeScreen>:
    BoxLayout:
        orientation: 'vertical'

        OriginalFlatKivyDemoLayout:


<-OriginalFlatKivyDemoLayout>:
    orientation: 'vertical'

    GridLayout:
        cols: 3
        pos: root.pos
        size: root.size
        padding: '5dp'
        spacing: '5dp'
        canvas.before:
            Color:
                rgb: 1,1,1
            Rectangle:
                pos: self.pos
                size: self.size

        FlatButton:
            text: 'button'
            theme: ('green', 'accent')

        FlatIconButton:
            text: 'icon button'
            icon: 'fa-tree'
            theme: ('green', 'accent')

        FlatToggleButton:
            text: 'toggle button'
            group: 'toggle'
            theme: ('green', 'accent')

        RaisedFlatToggleButton:
            text: 'raised toggle button'
            group: 'toggle'
            theme: ('green', 'accent')

        FlatCheckBoxListItem:
            text: 'check 1'
            group: 'check'
            theme: ('green', 'accent')

        FlatCheckBoxListItem:
            text: 'check 2'
            group: 'check'
            theme: ('green', 'accent')

        FlatCard:
            image_source: 'flat_kivy/AstroPic1.jpg'
            text: 'the card'
            color_tuple: ('Gray', '0000')

        FlatTextInput:

        BoxLayout:
            orientation: 'vertical'
            FlatLabel:
                text: 'FlatScrollView'
                size_hint_y: None
                height: '35dp'
                theme: ('green', 'main')

            FlatScrollView:
                do_scroll_x: False

                BoxLayout:
                    orientation: 'vertical'
                    height: '400dp'
                    size_hint_y: None
                    FlatLabel:
                        text: '1'
                    FlatLabel:
                        text: '2'
                    FlatLabel:
                        text: '3'
                    FlatLabel:
                        text: '4'
                    FlatLabel:
                        text: '5'
                    FlatLabel:
                        text: '6'

        RaisedFlatButton:
            text: 'popup'
            theme: ('green', 'accent')
            on_release: popup_demo.open()
            popup_demo: popup_demo.__self__

        FlatPopup:
            id: popup_demo
            title: 'Flat Popup Demo'
            size_hint: .6,.6
            on_parent: if self.parent: self.parent.remove_widget(self)

            BoxLayout:
                spacing: '5dp'
                padding: '5dp'
                RaisedFlatButton:
                    text: 'just a button in here'
                    theme: ('green', 'main')
                RaisedFlatButton:
                    text: 'just a button in here'
                    theme: ('green', 'main')

        FlatSlider:
            id: hor_slider
            orientation: 'horizontal'
            min: 10
            value: ver_slider.value
            theme: ('green', 'main')

        FlatSlider:
            id: ver_slider
            orientation: 'vertical'
            min: 10
            value: hor_slider.value
            theme: ('green', 'main')

        FlatSlider:
            value: hor_slider.value
            orientation: 'horizontal'
            disabled: True
            theme: ('green', 'main')
''')


Builder.load_file('flat_kivy_extensions/ui_elements.kv')

class HeaderLayout(BoxLayout):
    pass


class SomeScreen(Screen):
    pass

class OriginalFlatKivyDemoLayout(BoxLayout):
    pass


class RootWidget(Widget):
    pass


class ExtendedFlatApp(FlatApp):
    def __init__(self, app_config_entries, title, about, *largs, **kwargs):
        super(ExtendedFlatApp, self).__init__(*largs, **kwargs)
        self.title = title
        self.app_config_entries = app_config_entries
        self.about = about

    def build(self):
        self.root = RootWidget()
        self._navigationdrawer = self.root.ids.navigationdrawer
        self._side_panel = self.root.ids.side_panel
        self._header = self.root.ids.header
        self._screenmanager = self.root.ids.screenmanager
        self._menu_button = self._header.ids._menu_button
        self._menu_button.bind(on_press=lambda j: self._navigationdrawer.toggle_state())

        for entry in self.app_config_entries:
            if type(entry) == type(''):
                label = FlatLabel(text=entry)
                label.theme = ('green', 'main')
                label.size_hint_y = None
                label.height = '40dp'
                self._side_panel.add_widget(label)

            if type(entry) == type(tuple()):
                btnText = entry[0]
                btn = FlatIconButtonLeft(text=btnText,
                                size_hint_y=None, height='40dp',
                                icon='fa-chevron-right',
                                padding='3dp',
                                font_color_tuple=('Gray', '100'),
                                )
                btn.ids.icon.font_size = '15dp'
                btn.ids.icon.color_tuple = ('Brown', '100')
                btn.ids.label.font_size = '15dp'
                btn.ids.label.halign = 'left'
                # Question: why does it not work to specify color in the kwargs above
                btn.color = (.15, .15, .15)
                self._side_panel.add_widget(btn)

                btn.config = entry
                btn.screen = None
                btn.bind(on_release=self._switch_to_screen)

                self._create_screen(btn)

        self._side_panel.add_widget(Widget())

        return self.root

    def setup_themes(self):
        main = {
            'FlatButton': {
                'color_tuple': ('Gray', '0000'),
                'font_color_tuple': ('LightGreen', '800'),
                'style': 'Button',
                },
            'RaisedFlatButton': {
                'color_tuple': ('Gray', '0000'),
                'font_color_tuple': ('LightGreen', '800'),
                'style': 'Button',
                },
            'FlatLabel': {
                'style': 'Button',
                },
            'FlatSlider': {
                'bar_fill_color_tuple': ('LightGreen', '500'),
                'handle_accent_color_tuple': ('LightGreen', '200'),
                }
            }


        accent = {
            'FlatButton': {
                'color_tuple': ('LightGreen', '500'),
                'font_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                },
            'RaisedFlatButton': {
                'color_tuple': ('LightGreen', '500'),
                'font_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                },
            'FlatIconButton': {
                'color_tuple': ('LightGreen', '500'),
                'font_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                'icon_color_tuple': ('Gray', '1000')
                },
            'FlatToggleButton': {
                'color_tuple': ('LightGreen', '500'),
                'font_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                },
            'RaisedFlatToggleButton': {
                'color_tuple': ('LightGreen', '500'),
                'font_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                },
            'FlatCheckBox': {
                'color_tuple': ('Gray', '0000'),
                'check_color_tuple': ('LightGreen', '500'),
                'outline_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                'check_scale': .7,
                'outline_size': '10dp',
                },
            'FlatCheckBoxListItem': {
                'font_color_tuple': ('Gray', '1000'),
                'check_color_tuple': ('LightGreen', '500'),
                'outline_color_tuple': ('Gray', '800'),
                'style': 'Button',
                'check_scale': .7,
                'outline_size': '10dp',
                },
            }

        header = {
            'CustomIconButton': {
                'color_tuple': ('Brown', '500'),
                'font_color_tuple': ('Gray', '1000'),
                'style': 'Button',
                'icon_color_tuple': ('Gray', '1000'),
                },
                }

        self.theme_manager.add_theme('green', 'main', main)
        self.theme_manager.add_theme('green', 'accent', accent)
        self.theme_manager.add_theme('app', 'header', header)

        from flat_kivy_extensions.uix.customiconbutton import CustomIconButton
        self.theme_manager.types_to_theme['CustomIconButton'] = CustomIconButton

    def _create_screen(self, button):
        if button.screen is None:
            button.screen = button.config[1](*button.config[2], **button.config[3])
            self._screenmanager.add_widget(button.screen)

    def _switch_to_screen(self, instance):
        if instance.screen is None:
            self._create_screen(instance)
        self._screenmanager.current = instance.screen.name
        self._navigationdrawer.toggle_state()


