import os

import traceback, sys

#from navigationscreen import CoverFlowPopup
from flat_kivy_extensions.uix.coverflowpopup import CoverFlowPopup

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import mainthread, Clock
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition, NoTransition, ScreenManager
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen

from flat_kivy.flatapp import FlatApp
from flat_kivy.uix.flatlabel import FlatLabel
from flat_kivy.font_definitions import style_manager

from flat_kivy_extensions.uix import CustomPopupContent, CustomBusyContent, CustomErrorContent
from flat_kivy_extensions.uix.custompopup import CustomPopup
from flat_kivy_extensions.uix.customscreen import CustomScreen

from flat_kivy_extensions.uix.customiconbutton import CustomIconButton
from flat_kivy_extensions.uix.custombutton import CustomButton
from flat_kivy_extensions.uix.thumbnailwidget import ThumbNailWidget


from . import PackageLogger
log = PackageLogger(__name__, moduleDebug=True)


Builder.load_string('''
#:import NavigationDrawer kivy.garden.navigationdrawer.NavigationDrawer
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
<RootWidget>:
    title: 'Some App Title'
    background_color: 1.0, 1.0, 1.0
    header_height: dp(40)
    header_color: 0.1, 0.3, 0.2
    side_panel_color: [0.8, 0.9, 0.9, 1.0]

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

            ScrollView:
                id: side_panel_container
                canvas.before:
                    Color:
                        rgba: root.side_panel_color
                    Rectangle:
                        pos: self.pos
                        size: self.size

                #StackLayout:
                #    orientation: 'tb-lr'
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    id: side_panel
                    #orientation: 'vertical'
                    padding: '2dp'
                    spacing: '2dp'

                    canvas.before:
                        Color:
                            rgba: root.side_panel_color
                        Rectangle:
                            pos: self.pos
                            size: self.size

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
    menu_button_width: '40dp'
    title: 'Header'
    color: .1, .9, .1

    canvas.before:
        Color:
            rgb: root.color
        Rectangle:
            pos: self.pos
            size: self.size


    RelativeLayout:

        BoxLayout:
            id: _btn_layout
            padding: [dp(10), 0, 0, 0]

            CustomIconButton:
                id: _menu_button
                theme: ('app', 'header')
                icon: 'fa-bars'
                size_hint_x: None
                width: root.menu_button_width
                color: root.header_color

            #ProgressSpinner:
            CustomSpinner:
                id: _busy_indicator
                size_hint: (None, None)
                height: root.height
                width: root.height*0.5
                color: 0.9, 0.9, .9, 1
                stroke_width: dp(7.0)*0.5
                stroke_length: 20
                speed: 4.0

            # Widget:

        FlatLabel:
            text: root.title
            theme: ('app', 'header')
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            #center_x: root.center_x

            canvas.before:
                Color:
                    rgba: (.5, .6, .5, .0)
                Rectangle:
                    pos: self.pos
                    size: self.size



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


flat_kivy_extensions_path = os.path.dirname(os.path.abspath(__file__))
Builder.load_file('%s/ui_elements.kv' % flat_kivy_extensions_path)

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

    def add_widget(self, screen, *largs):
        super(CustomScreenManager, self).add_widget(screen, *largs)
        screen.bind(on_enter=self._on_screen_enter)
        self._thumbnailLut[screen] = BlankThumbNail(text='??',
                                            size_hint=(None, None),
                                            size=(Window.width*.75, Window.height*.75),
                                            )

    def _on_screen_enter(self, screen):
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

    @mainthread
    def _trigger_next_screen(self):
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
            log.info('Instantiating screen from class: %s' % (str(self.screen_class.__name__)))
            self._screen = self.screen_class(*self.screen_args, **self.screen_kwargs)
            self._screen.name = self.screen_name
        return self._screen

    screen = property(_getScreen)


class NavDrawerEntryConfig(ScreenConfig):

    def __init__(self, screen_class, button_title=None, button_icon='', screen_args=[], screen_kwargs={}):
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
        if self.button_icon is not None:
            btn.icon = self.button_icon
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
        self.root = RootWidget()

        self._busy_counter = 0

        self.stop_callbacks = list()
        self.start_callbacks = list()

    def build(self):
        #self.root = RootWidget()
        self.root.title = self.title
        self._navigationdrawer = self.root.ids.navigationdrawer
        self._side_panel = self.root.ids.side_panel
        self._header = self.root.ids.header
        self._screenmanager = self.root.ids.screenmanager
        self._menu_button = self._header.ids._menu_button
        self._busy_indicator = self._header.ids._busy_indicator.__self__
        self._header_button_layout = self._header.ids._btn_layout
        self._header_button_layout.remove_widget(self._busy_indicator)
        self._busy_indicator.stop_spinning()

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

        return self.root

    def setup_themes(self):

        # Add default application themes
        from themes_and_fonts import themes, types_to_theme
        self.add_themes(themes, types_to_theme)

        # Add user themes if specified
        if self._themes is not None:
            self.add_themes(self._themes, self._types_to_theme)


    def add_themes(self, themes, types_to_theme={}):
        for (theme, value) in themes.items():
            for (variant, theme_dict) in value.items():
                if theme in self.theme_manager.themes.keys():
                    if variant in self.theme_manager.themes[theme].keys():
                        _value = self.theme_manager.themes[theme][variant]
                        for (className, properties) in themes[theme][variant].items():
                            _value[className] = properties
                    else:
                        self.theme_manager.add_theme(theme, variant, theme_dict)
                else:
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

    def show_busy_in_header(self, state=True):
        if state:
            if self._busy_indicator not in self._header_button_layout.children:
                self._header_button_layout.add_widget(self._busy_indicator)
                self._busy_indicator.start_spinning()
                #Clock.unschedule(self._busy_indicator._update)
        else:
            if self._busy_indicator in self._header_button_layout.children:
                self._header_button_layout.remove_widget(self._busy_indicator)
                self._busy_indicator.stop_spinning()

    def indicate_busy(self, value):
        if value:
            self._busy_counter += 1
        else:
            if self._busy_counter == 0:
                log.debug('Busy counter is already 0 - there should be nothing showing')
            else:
                self._busy_counter += -1
        self.show_busy_in_header(self._busy_counter>0)

    def raise_busy(self, busy_title, busy_text, auto_dismiss=False, timeout=None, cancel_callback=None, timeout_callback=None):
        busy_content = CustomBusyContent()
        busy_content.theme=('app', 'shit')
        self.busy_popup = CustomPopup(
            content=busy_content, size_hint=(None, None), width=dp(200),
            auto_dismiss=auto_dismiss,
            separator_color=(0,0,0,1),
            background_color=(0,0,0,.25),
            separator_height=dp(1),)

        busy_content.popup = self.busy_popup
        busy_content.bind(height=self._update_popup_height)
        busy_content.label_color_tuple = ('BlueGray', '800')
        busy_content.cancel_btn_color_tuple = ('BlueGray', '700')

        self.busy_popup.title_color_tuple = ('BlueGray', '700')
        self.busy_popup.title_size = dp(13)
        self.busy_popup.popup_color=(.95, .95, .95, 1.0)

        #Clock.unschedule(busy_content.spinner._update)
        #Clock.schedule_interval(busy_content.spinner._update, .5)
        busy_content.spinner.start_spinning()

        busy_content.busy_text = busy_text
        self.busy_popup.title = busy_title
        cancel_button = busy_content.cancel_button
        event = None
        def dismiss_popup(*largs):
            busy_content.spinner.stop_spinning()
            if event is not None:
                event.cancel()
            self.busy_popup.dismiss()
            if cancel_callback is not None:
                cancel_callback()
        #dismiss_button.bind(on_release=self.busy_popup.dismiss)
        cancel_button.bind(on_release=dismiss_popup)
        self.busy_popup.open()

        if timeout is not None:
            def close_popup(dt):
                busy_content.spinner.stop_spinning()
                self.busy_popup.dismiss()
                if timeout_callback is not None:
                    timeout_callback()
            event = Clock.schedule_once(close_popup, timeout)
            def clear_timeout(self):
                event.cancel()
            self.busy_popup.bind(on_dismiss=clear_timeout)
        return self.busy_popup

    #def _update_busy_popup_height(self, instance, value):
    #    instance.popup.height = value + dp(33)

    def raise_dialog(self, title, text, auto_dismiss=False, okay_callback=None, cancel_callback=None, timeout=None):
        content = CustomPopupContent()
        content.text = text
        content.label_color_tuple = ('BlueGray', '800')
        content.cancel_text = 'Dismiss'
        content.ok_text = 'Sure'

        if okay_callback is None and cancel_callback is None:
            content.btn_layout.remove_widget(content.cancel_button)
            content.ok_text = 'Okay'

        self.popup = CustomPopup(
            content=content, size_hint=(None, None), width=dp(200),
            auto_dismiss=auto_dismiss,
            separator_color=(0,0,0,1),
            background_color=(0,0,0,0.25),
            separator_height=dp(1),)

        content.cancel_btn_color_tuple = ('BlueGray', '700')
        content.ok_btn_color_tuple = ('BlueGray', '700')

        content.popup = self.popup
        content.bind(height=self._update_popup_height)

        self.popup.title_color_tuple = ('BlueGray', '700')
        self.popup.popup_color=(.95, .95, .95, 1.0)
        self.popup.title = title
        self.popup.title_size = dp(13)
        self.popup.height = content.minimum_height - dp(10)

        cancel_button = content.cancel_button
        cancel_button.bind(on_release=self.popup.dismiss)

        def receivedOkay(*largs):
            self.popup.dismiss()
            if okay_callback is not None:
                okay_callback()

        def receivedCancel(*largs):
            self.popup.dismiss()
            if cancel_callback is not None:
                cancel_callback()

        ok_button = content.ok_button
        ok_button.bind(on_release=receivedOkay)

        cancel_button = content.cancel_button
        cancel_button.bind(on_release=receivedCancel)

        self.popup.open()

        return self.popup

    def _update_popup_height(self, instance, value):
        instance.popup.height = value + dp(33)
#        print(' window center y: %s' % str(Window.height))
#        print(' popup pos : %s' % str(instance.popup.pos))
        y_pos = Window.height/2 - instance.popup.height/2
        instance.popup.pos = (instance.popup.pos[0],  y_pos)


    def raise_error(self, error_title, error_text, auto_dismiss=False, timeout=None):
        error_content = CustomErrorContent()
        error_content.error_text = error_text
        error_content.label_color_tuple = ('BlueGray', '800')

        self.error_popup = CustomPopup(
            content=error_content, size_hint=(None, None), width=dp(200),
            auto_dismiss=auto_dismiss,
            separator_color=(0,0,0,1),
            background_color=(0,0,0,0.25),
            separator_height=dp(1),
            cols=1,)
        error_content.popup = self.error_popup
        error_content.cancel_btn_color_tuple = ('BlueGray', '700')

        self.error_popup.title_color_tuple = ('BlueGray', '700')
        self.error_popup.popup_color=(.95, .95, .95, 1.0)
        self.error_popup.title = error_title
        self.error_popup.title_size = dp(13)
        self.error_popup.height = error_content.minimum_height + dp(50)

        error_content.bind(height=self._update_popup_height)
        cancel_button = error_content.cancel_button
        cancel_button.text = 'Ok'
        cancel_button.bind(on_release=self.error_popup.dismiss)
        error_content.theme=('app', 'shit')

        log.error(error_text)
        #print(traceback.format_exc())
        #print(sys.exc_info())
        #print( traceback.print_stack()  )
        self.error_popup.open()
        if timeout is not None:
            def close_popup(dt):
                self.error_popup.dismiss()
            Clock.schedule_once(close_popup, timeout)

        return self.error_popup

    #def _update_error_popup_height(self, instance, value):
    #    instance.popup.height = value + dp(33)
#
    def _create_navigation_label(self, entry):
        label = FlatLabel(text=entry.get('text', 'None'))
        if 'theme' in entry.keys():
            setattr(label, 'theme', entry['theme'])
            del(entry['theme'])
        else:
            setattr(label, 'theme', ('app', 'navigationdrawer'))
        for (key,value) in entry.items():
            setattr(label, key, value)
        if entry != self.app_config_entries[0]:
            self._side_panel.add_widget(Widget(size_hint_y=None, height=dp(15)))
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
        if screen not in self._screenmanager.screens:
            self._screenmanager.add_widget(screen)
        self._screenmanager.current = screen.name
        self._navigationdrawer.toggle_state()

    def on_pause(self):
        log.info("Pausing application.")
        return True

    def register_stop_callback(self, callback):
        ''' Register a function or method that should be called
        as the application is shutting down.
        '''
        self.stop_callbacks.append(callback)

    def on_stop(self):
        log.info('Stopping application')
        for callback in self.stop_callbacks:
            callback()
        return False


    def register_start_callback(self, callback):
        ''' Register a function or method that should be called
        as the application is shutting down.
        '''
        self.start_callbacks.append(callback)

    def on_start(self):
        log.info('Starting application')
        for callback in self.start_callbacks:
            callback()
        return False



