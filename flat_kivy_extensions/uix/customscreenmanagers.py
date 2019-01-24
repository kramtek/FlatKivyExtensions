

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from flat_kivy_extensions.flatappextension import CustomScreenManager, ScreenNavigationEntry
from flat_kivy_extensions.uix.customscreen import CustomScreen
Builder.load_string('''
<-TabButtonLayout>:
    canvas.before:
        Color:
            rgba: (.5, .5, .5, 1.0)
        Rectangle:
            size: self.size
            pos: self.pos
''')


class CustomTabScreen(Screen):

    def __init__(self, screen_config_entries, **kwargs):
        self._isSetup = False
        super(CustomTabScreen, self).__init__(**kwargs)
        self._screen_config_entries = screen_config_entries

#    def on_enter(self):
        if self._isSetup:
            return
        self._screenmanager = CustomScreenManager()
        self._screenmanager.transition = FadeTransition(duration=0.0)
        self.add_widget(self._screenmanager)
        self.title = ''

        self.btns = list()
        for entry in self._screen_config_entries:
            if isinstance(entry, ScreenNavigationEntry):
                self._create_navigation_button(entry)

        self.tabButtonLayout = TabButtonLayout(self.btns)

        self.add_widget(self.tabButtonLayout)
        self.tabButtonLayout._btn_pressed(self.btns[0])
        self._isSetup = True

    def _create_navigation_button(self, entry):
        btn = entry.create_button(self._screenmanager)
        btn.theme = ('app', 'tabbarbutton')
        if entry.button_icon is not None:
            btn.icon = entry.button_icon
        btn.bind(on_release=self._switch_to_screen)
        screen = btn.config.screen
        if isinstance(screen, CustomScreen):
            screen.outer_container.add_widget(Widget(size_hint_y=None, height=dp(56)))
        self._screenmanager.add_widget(screen)
        self.btns.append(btn)

    def _switch_to_screen(self, instance):
        screen = instance.config.screen
        if screen not in self._screenmanager.screens:
            self._screenmanager.add_widget(screen)
        self._screenmanager.current = screen.name


    def on_pre_enter(self):
        self._screenmanager.current_screen.on_pre_enter()

    def on_enter(self):
        self._screenmanager.current_screen.on_enter()

    def on_pre_leave(self):
        self._screenmanager.current_screen.on_pre_leave()

    def on_leave(self):
        self._screenmanager.current_screen.on_leave()


class TabButtonLayout(BoxLayout):

    def __init__(self, btns, **kwargs):
        super(TabButtonLayout, self).__init__(**kwargs)
        self.spacing = dp(1)
        self.padding = dp(1)
        self.size_hint_y = None
        self.height = dp(55)
        self.btns = btns

        for btn in btns:
            self.add_widget(btn)
            btn.height = self.height - 2*self.padding[0]
            btn.bind(on_release=self._btn_pressed)

    def _btn_pressed(self, instance):
        for btn in self.btns:
            btn.theme = ('app', 'tabbarbutton')
        instance.theme = ('app', 'tabbarbutton_highlighted')


