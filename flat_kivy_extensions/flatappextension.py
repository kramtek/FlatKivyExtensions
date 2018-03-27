import time, threading

from navigationscreen import CoverFlowPopup

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import FadeTransition, NoTransition, ScreenManager
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar

from flat_kivy.flatapp import FlatApp
from flat_kivy.uix.flatlabel import FlatLabel
from flat_kivy.font_definitions import style_manager

from flat_kivy_extensions.uix.customiconbutton import CustomIconButton
from flat_kivy_extensions.uix.custombutton import CustomButton
from flat_kivy_extensions.uix.thumbnailwidget import ThumbNailWidget

# import flat_kivy
# flat_kivy_font_path = os.path.join(os.path.dirname(os.path.abspath(flat_kivy.__file__)), *['data', 'font'])
# import flat_kivy_extensions
# extensions_font_path = os.path.join(os.path.dirname(os.path.abspath(flat_kivy_extensions.__file__)), *['data', 'font'])
#
# paths = [flat_kivy_font_path, extensions_font_path]
# common_prefix = os.path.commonprefix(paths)
# relative_paths = [os.path.relpath(path, common_prefix) for path in paths]
# components = relative_paths[0].split(os.sep)
# relative_path_to_extensions  = os.sep.join(['..']*len(components))
# relative_path_to_fonts  = os.path.join(relative_path_to_extensions, relative_paths[1])

Builder.load_string('''
#:import NavigationDrawer kivy.garden.navigationdrawer.NavigationDrawer
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
<RootWidget>:
    title: 'Some App Title'
    background_color: 1.0, 1.0, 1.0
    header_height: dp(40)
    header_color: 0.1, 0.3, 0.2
    side_panel_color: 0.1, 0.1, 0.1

    BoxLayout:
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
            header_color: root.header_color

        NavigationDrawer:
            id: navigationdrawer
            height: root.height
            width: root.width
            side_panel_width: min(dp(250), 0.6*self.width)
            anim_type:  'slide_above_simple'

            StackLayout:
                orientation: 'tb-lr'
                id: side_panel
                #orientation: 'vertical'
                padding: '3dp'
                spacing: '3dp'

                # this will be populated dynamically when the root application is built

            BoxLayout:
                orientation: 'vertical'

                canvas.before:
                    Color:
                        rgb: root.background_color
                    Rectangle:
                        pos: self.pos
                        size: self.size

                CustomScreenManager:
                    id: screenmanager
                    padding: '10dp'
                    transition: NoTransition()
                    # Question: When selecting FadeTransition the switching
                    #           annimation seems to go black when switching,
                    #           how can this be avoided?
                    #transition: FadeTransition(duration=5.0)
                    canvas.before:
                        Color:
                            rgb: root.background_color
                        Rectangle:
                            pos: self.pos
                            size: self.size


<-HeaderLayout>:
    header_height: '40dp'
    header_color: 0.2, 0.1, 0.2
    menu_button_width: '50dp'
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
        width: root.menu_button_width
        color: root.header_color

    FlatLabel:
        text: root.title
        theme: ('app', 'header')

<-BlankThumbNail>:
    text: 'hi'
    canvas.before:
        Color:
            rgba: (.9, .9, .9, .9)
        Rectangle:
            pos: self.pos
            size: self.size

    FlatLabel:
        text: root.text
        color_tuple: ('Green', '900')

''')


Builder.load_file('flat_kivy_extensions/ui_elements.kv')

class HeaderLayout(BoxLayout):
    pass

class RootWidget(Widget):
    pass

class BlankThumbNail(FlatLabel):
    pass

class CustomScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super(CustomScreenManager, self).__init__(**kwargs)
        self._thumbnailLut = dict()
        self._open_screen_index = -1
        self._current_screen = None;

        # self._is_opening = False

    def add_widget(self, screen, *largs):
        super(CustomScreenManager, self).add_widget(screen, *largs)
        screen.bind(on_enter=self._on_screen_enter)
        self._thumbnailLut[screen] = BlankThumbNail(text='??',
                                            size_hint=(None, None),
                                            size=(Window.width*.75, Window.height*.75),
                                            )

    def _on_screen_enter(self, screen):
        print 'current screen: %s' % str(self.current_screen)
        if self._open_screen_index >= 0:
            if isinstance(self._thumbnailLut[screen], BlankThumbNail):
                self._thumbnailLut[screen] = ThumbNailWidget(screen)
            self.pb.value = len(self.screens) - self._open_screen_index
            self._trigger_next_screen()

    def get_all_thumbnails(self, callback=None):
        self._current_screen = self.current_screen
        no_need_to_generate = True
        for screen in self.screens:
            if isinstance(self._thumbnailLut[screen], BlankThumbNail):
                no_need_to_generate = False
                break
        if no_need_to_generate:
            callback()
            return

        self._callback = callback

        # Display a modal view to indicate screen loading progress
        self.mv = ModalView(size_hint=(None, None), size=(0,0), background_color=(.1, .1, .1, 0.95))
        self.lbl = FlatLabel(text='Loading Screens...', style='CustomButton1')
        self.pb = ProgressBar(max=len(self.screens), value=1)
        self.pb.size_hint = (None, None)
        self.pb.size = (dp(200), dp(40))
        layout = BoxLayout(orientation='vertical', size_hint = (None, None), size=(dp(200), dp(80)))
        layout.add_widget(self.lbl)
        layout.add_widget(self.pb)
        self.mv.add_widget(layout)
        self.mv.auto_dismiss = False
        self.mv.bind(on_open=self._continue)
        self.mv.open()

    def _continue(self, mv):
        self._open_screen_index = len(self.screens) - 1
        self._trigger_next_screen()
        # threading.Thread(target=self._wait_for_thumbnails).start()

    # def _wait_for_thumbnails(self):
    #     while self._open_screen_index >= 0:
    #         time.sleep(0.25)
    #     self.mv.dismiss()
    #     if self._callback is not None:
    #         self._callback()

    @mainthread
    def _trigger_next_screen(self):
        print 'screen index: %s'  % str(self._open_screen_index)
        while self._open_screen_index >= 0:
            screen = self.screens[self._open_screen_index]

            if isinstance(self._thumbnailLut[screen], BlankThumbNail):
                self.current = screen.name
                return
            self._open_screen_index -= 1
        self.mv.dismiss()
        if self._callback is not None:
            self._callback()

    def show_navigation_popup(self):
        thumbnails = list()
        for screen in self.screens:
            thumbnails.append( self._thumbnailLut[screen] )
        print 'current screen: %s' % str(self.current_screen)
        navigation_popup = CoverFlowPopup(thumbnails, self._index_selected, self.screens.index(self._current_screen))
        navigation_popup.open()

    def _index_selected(self, index):
        self.current = self.screens[index].name


class ScreenConfig(object):

    def __init__(self, screen_class, screen_args=[], screen_kwargs={}, screen_name=None):
        self.screen_class = screen_class
        self.screen_args = screen_args
        self.screen_kwargs = screen_kwargs
        self.screen_name = screen_name
        self._screen = None

    def add_to_screen_manager(self, screenmanager):
        if self._screen is None:
            self._screen = self.screen_class(*self.screen_args, **self.screen_kwargs)
        if self._screen not in self._screenmanager.screens:
            screenmanager.add_widget(self._screen)
        return self._screen

    def _getScreen(self):
        if self._screen is None:
            print('Instantiating screen from class: %s' % (str(self.screen_class.__name__)))
            self._screen = self.screen_class(*self.screen_args, **self.screen_kwargs)
            self._screen.name = self.screen_name
        return self._screen

    screen = property(_getScreen)


class NavDrawerEntryConfig(ScreenConfig):

    def __init__(self, screen_class, button_title=None, button_icon=None, screen_args=[], screen_kwargs={}):
        if button_title is None:
            button_title = screen_class.__name__
        self.button_title = button_title
        self.button_icon = button_icon
        super(NavDrawerEntryConfig, self).__init__(screen_class, screen_args=screen_args, screen_kwargs=screen_kwargs, screen_name=button_title)

    def create_button(self, screenmanager):
        btn = CustomIconButton(text=self.button_title)
        btn.theme = ('app', 'navigationdrawer')
        btn.config = self
        btn.manager = screenmanager
        return btn


class ExtendedFlatApp(FlatApp):
    def __init__(self, app_config_entries, title, about,
                 use_coverflow_navigation=True,
                 lazy_loading=False,
                 themes={}, types_to_theme={}, font_styles={},
                 **kwargs):
        self._themes = themes
        self._types_to_theme = types_to_theme
        self._font_styles = font_styles
        super(ExtendedFlatApp, self).__init__(**kwargs)
        self.title = title
        self.app_config_entries = app_config_entries
        self.about = about
        self.lazy_loading = lazy_loading
        self._use_coverflow_navigation = use_coverflow_navigation
        self._first_screen = None
        self._first_navigation_label = None

    def build(self):
        self.root = RootWidget()
        self._navigationdrawer = self.root.ids.navigationdrawer
        self._side_panel = self.root.ids.side_panel
        self._header = self.root.ids.header
        self._screenmanager = self.root.ids.screenmanager
        self._menu_button = self._header.ids._menu_button

        self._menu_button.bind(on_press=lambda j: self._navigationdrawer.toggle_state())

        for entry in self.app_config_entries:
            if type(entry) not in [type(str()), type(dict())] and not isinstance(entry, NavDrawerEntryConfig):
                raise Exception('Each item in the application config entries list must either be a string, dict, or instance of NavDrawerEntryConfig')
            if type(entry) == type(str()):
                entry = {'text' : entry, 'theme' : ('app', 'navigationdrawer')}
            if type(entry) == type(dict()):
                self._create_navigation_label(entry)
            if isinstance(entry, NavDrawerEntryConfig):
                self._create_navigation_button(entry)

        # if not self.use_coverflow_navigation:
        #     return self.root

        # self._screenmanager.get_all_thumbnails()

        return self.root

        # self._thumbnails = list()
        # self._is_opening = True
        # self._open_screen_index = len(self._screenmanager.screens)-1
        # self.open_all_screens()
        #
        # return self.root

#    @mainthread
#    def open_all_screens(self):
#        screen = self._screenmanager.screens[self._open_screen_index]
#        screen.bind(on_enter=self._local_on_enter)
#        self._screenmanager.current = screen.name
#
#    def _local_on_enter(self, screen):
#        if not self._is_opening:
#            return
#        thumbnail = ThumbNailWidget(screen)
#        thumbnail.name = screen.name
#        self._thumbnails.append(thumbnail)
#        self._open_screen_index -= 1
#        if self._open_screen_index >= 0:
#            self.open_all_screens()
#        else:
#            self.finalize()
#
#    @mainthread
#    def finalize(self):
#        self.navigation_popup = CoverFlowPopup(self._thumbnails)
#        self.navigation_popup.size_hint = (None, None)
#        self.navigation_popup.size = (0,0)
#        self.navigation_popup.background_color = (.0, .0, .0, .9)
#        self._is_opening = False
#        self._screenmanager.transition = FadeTransition()
#        # self._menu_button.bind(on_press=lambda j: self.navigation_popup.open())

    def setup_themes(self):

        # Add default application themes
        from themes_and_fonts import themes, types_to_theme
        self.add_themes(themes, types_to_theme)

        # Add user themes if specified
        self.add_themes(self._themes, self._types_to_theme)


    def add_themes(self, themes, types_to_theme={}):
        for (theme, value) in themes.items():
            for (variant, theme_dict) in value.items():
                self.theme_manager.add_theme(theme, variant, theme_dict)
        for (key,value) in types_to_theme.items():
            self.theme_manager.types_to_theme[key] = value

    def setup_font_ramps(self):
        super(ExtendedFlatApp, self).setup_font_ramps()

        # Load application default font styles
        from themes_and_fonts import font_styles
        self.add_font_styles(font_styles)

    def add_font_styles(self, font_styles):
        for each in font_styles:
            style = font_styles[each]
            sizings = style['sizings']
            style_manager.add_style(style['font'], each, sizings['mobile'],
                sizings['desktop'], style['alpha'])

    # def _create_navigation_label_from_string(self, entry):
    #     entry = {'text' : entry, 'theme' : ('app', 'navigationdrawer')}
    #     if self._first_navigation_label is None:
    #         self._first_navigation_label = self._create_navigation_label_from_dict(entry)
    #         return
    #     entry['style'] = 'NavigationLabelSubHeading'
    #     self._create_navigation_label_from_dict(entry)

    def _create_navigation_label(self, entry):
        label = FlatLabel(text=entry.get('text', 'None'))
        if 'theme' in entry.keys():
            setattr(label, 'theme', entry['theme'])
            del(entry['theme'])
        else:
            setattr(label, 'theme', ('app', 'navigationdrawer'))
        for (key,value) in entry.items():
            setattr(label, key, value)
        self._side_panel.add_widget(label)
        return label

    def _create_navigation_button(self, entry):
        btn = entry.create_button(self._screenmanager)
        self._side_panel.add_widget(btn)
        btn.bind(on_release=self._switch_to_screen)
        if len(self._screenmanager.children) == 0:
            self._screenmanager.add_widget(btn.config.screen)
        else:
            if not self.lazy_loading:
                self._screenmanager.add_widget(btn.config.screen)

    def _switch_to_screen(self, instance):
        screen = instance.config.screen
        print 'switching to screen: %s'  % str(screen)
        if screen not in self._screenmanager.screens:
            self._screenmanager.add_widget(screen)
        self._screenmanager.current = screen.name
        self._navigationdrawer.toggle_state()


