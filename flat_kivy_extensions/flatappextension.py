

import os, platform

from kivy.garden import garden_system_dir
print('Garden system dir: %s\n\n\n' % str(garden_system_dir))

from flat_kivy_extensions.uix.coverflowpopup import CoverFlowPopup

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import mainthread, Clock
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition, NoTransition, ScreenManager
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty

from flat_kivy.flatapp import FlatApp
from flat_kivy.uix.flatlabel import FlatLabel
from flat_kivy.font_definitions import style_manager

from flat_kivy_extensions.uix import CustomPopupContent, CustomBusyContent, CustomErrorContent
from flat_kivy_extensions.uix.custompopup import CustomPopup
from flat_kivy_extensions.uix.customscreen import CustomScreen

from flat_kivy_extensions.uix.customiconbutton import CustomIconButton
from flat_kivy_extensions.uix.custombutton import CustomButton
from flat_kivy_extensions.uix.thumbnailwidget import ThumbNailWidget

if 'KIVY_DOC' in os.environ:
    from navigationdrawer import NavigationDrawer
    from pizza import Pizza
else:
    from kivy.garden.navigationdrawer import NavigationDrawer
    from flat_kivy_extensions.uix.customicon import CustomIcon

from . import PackageLogger
log = PackageLogger(__name__, moduleDebug=True)

log.info('\n\n\n')
log.info('Platform system: %s     machine: %s' % (str(platform.system()), str(platform.machine())))
log.info('Garden system dir: %s\n\n\n' % str(garden_system_dir))

Builder.load_string('''
## #:import NavigationDrawer kivy.garden.navigationdrawer.NavigationDrawer
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
            menu_width: min(dp(250), 0.6*self.width)
            dashboard_width: 0.95*self.width
            side_panel_width: self.menu_width if not root.use_dashboard_navigation else self.dashboard_width
            #anim_type:  'slide_above_simple'
            anim_type:  'fade_in'
            main_layout: main_layout.__self__

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
                #BlockingGridLayout:
                    id: side_panel
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    #orientation: 'vertical'
                    padding: '2dp'
                    spacing: '2dp'

                    #canvas.before:
                    #    Color:
                    #        rgba: root.side_panel_color
                    #    Rectangle:
                    #        pos: self.pos
                    #        size: self.size

                # this will be populated dynamically when the root application is built

            BlockingBoxLayout:
                id: main_layout
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
    use_dashboard_navigation = BooleanProperty(False)

    def __init__(self, *largs, **kwargs):
        super(RootWidget, self).__init__(*largs, **kwargs)


class BlankThumbNail(FlatLabel):
    pass

#class BlockingGridLayout(GridLayout):
class BlockingBoxLayout(BoxLayout):

    block_ui = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.block_ui:
            return True
        return super(BlockingBoxLayout, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.block_ui:
            return True
        return super(BlockingBoxLayout, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.block_ui:
            return True
        return super(BlockingBoxLayout, self).on_touch_move(touch)

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


class BlockingIconButton(CustomIconButton):

    pass

#    def on_touch_down(self, touch):
#        return True
#
#    def on_touch_up(self, touch):
#        return True
#
#    def on_touch_move(self, touch):
#        return True


class ScreenNavigationEntry(ScreenConfig):

    def __init__(self, screen_class, button_title=None, button_icon='', screen_args=[], screen_kwargs={}):
        if button_title is None:
            button_title = screen_class.__name__
        self.button_title = button_title
        self.button_icon = button_icon
        super(ScreenNavigationEntry, self).__init__(screen_class, screen_args=screen_args, screen_kwargs=screen_kwargs, screen_name=button_title)

    def create_button(self, screenmanager):
        #btn = CustomIconButton(text=self.button_title)
        btn = BlockingIconButton(text=self.button_title)
        btn.theme = ('app', 'navigationdrawer')
        btn.config = self
        btn.manager = screenmanager
        if self.button_icon is not None:
            btn.icon = self.button_icon
        return btn



class ExtendedFlatApp(FlatApp):
    ''' Extension of FlatApp
    '''
    def __init__(self, app_config_entries, title, about,
                 use_coverflow_navigation=True,
                 lazy_loading=False,
                 use_dashboard_navigation=False,
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
        self.use_dashboard_navigation = use_dashboard_navigation

        self.root = RootWidget(use_dashboard_navigation=use_dashboard_navigation)

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

        if self.use_dashboard_navigation:
            self._side_panel.cols = 5

        index_offset = 0
        self.nav_buttons = list()
        for index, entry in enumerate(self.app_config_entries):
            if type(entry) not in [type(str()), type(dict())] and not isinstance(entry, ScreenNavigationEntry):
                raise Exception('Each item in the application config entries list must either be a string, dict, or instance of ScreenNavigationEntry')
            if type(entry) == type(str()):
                entry = {'text' : entry, 'theme' : ('app', 'navigationdrawer')}
            if type(entry) == type(dict()):
                index_offset += self._create_navigation_label(entry, index_offset, self._side_panel.cols)
            if isinstance(entry, ScreenNavigationEntry):
                btn = self._create_navigation_button(entry)
                self.nav_buttons.append(btn)
                index_offset += 1

        # Use for docked navigation
        if self.use_dashboard_navigation:
            #self._navigationdrawer.side_panel_darkness = 0.5
            #self._navigationdrawer.side_panel_opacity = 0.1
            self.root.side_panel_color = self.root.header_color # (0.1, 0.1, 0.1, 0.2)
            #self.root.side_panel_color = (0.1, 0.4, 0.1, 0.2)

        self._switch_to_screen(self.nav_buttons[0], toggle_state=False)

        if self.use_dashboard_navigation:
            self._side_panel.width = 0.95*self._side_panel.width
        self._navigationdrawer.bind(state=self._navdrawer_changed_state)
        return self.root

    def _navdrawer_changed_state(self, instance, value):
        layout = self._navigationdrawer.main_layout
        layout.block_ui = value.strip().startswith('open')

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

    def _getCustomPopup(self, content, auto_dismiss):
        popup = CustomPopup(
            content=content, size_hint=(None, None), width=dp(200),
            auto_dismiss=auto_dismiss,
            separator_color=(0,0,0,1),
            background_color=(0,0,0,.25),
            separator_height=dp(1),)

        popup.title_color_tuple = ('BlueGray', '700')
        popup.title_size = dp(13)
        popup.popup_color=(.95, .95, .95, 1.0)

        content.label_color_tuple = ('BlueGray', '800')
        content.btn_color_tuple = ('BlueGray', '700')
        content.bind(size=self._update_popup_size)
        content.popup = popup

        return popup

    def raise_busy(self, title, message, auto_dismiss=False, timeout=None, cancel_callback=None, timeout_callback=None, auto_open=True):
        content = CustomPopupContent()
        content.message = message
        content.cancel_text = 'Dismiss'
        content.remove_icon()
        content.remove_ok_btn()

        popup = self._getCustomPopup(content, auto_dismiss=auto_dismiss)
        popup.title = title

        cancel_button = content.cancel_button

        event = None
        def dismiss_popup(*largs):
            content.spinner.stop_spinning()
            if event is not None:
                event.cancel()
            popup.dismiss()
            if cancel_callback is not None:
                cancel_callback()
        cancel_button.bind(on_release=dismiss_popup)

        if timeout is not None:
            def close_popup(dt):
                content.spinner.stop_spinning()
                popup.dismiss()
                if timeout_callback is not None:
                    timeout_callback()
            event = Clock.schedule_once(close_popup, timeout)
            def clear_timeout(self):
                event.cancel()
            popup.bind(on_dismiss=clear_timeout)

        self._busy_popup = popup
        if auto_open:
            popup.open()
        return popup


    def raise_dialog(self, title, text, auto_dismiss=False, okay_callback=None, cancel_callback=None, timeout=None, auto_open=True):
        content = CustomPopupContent()
        content.message = text
        content.cancel_text = 'Dismiss'
        content.ok_text = 'Sure'

        content.remove_spinner()
        content.remove_icon()

        if okay_callback is None and cancel_callback is None:
            content.remove_cancel_btn()
            content.ok_text = 'Okay'

        popup = self._getCustomPopup(content, auto_dismiss=auto_dismiss)
        popup.title = title

        popup.height = content.minimum_height - dp(10)

        cancel_button = content.cancel_button

        event = None
        def dismiss_popup(*largs):
            content.stop_spinning(None)
            if event is not None:
                event.cancel()
            popup.dismiss()
            if cancel_callback is not None:
                cancel_callback()
        cancel_button.bind(on_release=dismiss_popup)

        def receivedOkay(*largs):
            popup.dismiss()
            if okay_callback is not None:
                okay_callback()

        def receivedCancel(*largs):
            popup.dismiss()
            if cancel_callback is not None:
                cancel_callback()

        content.ok_button.bind(on_release=receivedOkay)
        content.cancel_button.bind(on_release=receivedCancel)

        popup.bind(on_dismiss=content.stop_spinning)

        self._popup = popup
        if auto_open:
            popup.open()
        #content.stop_spinning()
        return popup

    def raise_error(self, error_title, error_text, auto_dismiss=False, timeout=None, auto_open=True, traceback=None):
        log.error(error_text)
        if traceback is not None:
            print(str(traceback))
        content = CustomErrorContent()
        content.message = error_text
        content.label_color_tuple = ('BlueGray', '800')

        popup = self._getCustomPopup(content, auto_dismiss=auto_dismiss)
        popup.title = error_title

        popup.height = content.minimum_height + dp(50)

        cancel_button = content.cancel_button
        cancel_button.text = 'Ok'
        cancel_button.bind(on_release=popup.dismiss)

        if timeout is not None:
            def close_popup(dt):
                popup.dismiss()
            Clock.schedule_once(close_popup, timeout)

        self.error_popup = popup
        if auto_open:
            popup.open()
        return self.error_popup

    def _update_popup_size(self, instance, value):
        instance.popup.height = value[1] + dp(33)
        y_pos = Window.height/2 - instance.popup.height/2
        instance.popup.pos = (instance.popup.pos[0],  y_pos)

    def _create_navigation_label(self, entry, index, cols):
        label = FlatLabel(text=entry.get('text', 'None'))
        if 'theme' in entry.keys():
            setattr(label, 'theme', entry['theme'])
            del(entry['theme'])
        else:
            setattr(label, 'theme', ('app', 'navigationdrawer'))
        for (key,value) in entry.items():
            setattr(label, key, value)
        # Use for docked
        if self.use_dashboard_navigation:
            label.color_tuple = ('Gray', '0000')
            #label.size_hint_x = 2.0
            label.text_size = (dp(150), dp(35))
            label.halign = 'left'
            label.valign = 'center'
        else:
            # Disable for docked navigation
            if entry != self.app_config_entries[0]:
                self._side_panel.add_widget(Widget(size_hint_y=None, height=dp(15)))

        added = 0
        # Use for docked
        if self.use_dashboard_navigation:
            # ... we need to add blank widgets to fill up previous row
            rng = (index%cols)
            if rng > 0:
                for colindex in xrange(cols-rng+1):
                    self._side_panel.add_widget(Widget())
                    added += 1
            else:
                self._side_panel.add_widget(Widget())
                added += 1

        self._side_panel.add_widget(label)
        added += 1

        if self.use_dashboard_navigation:
            # ... we need to add blank widgets to fill up current row
            for colindex in xrange(cols-2):
                self._side_panel.add_widget(Widget())
                added += 1

        return added

    def _configure_docked_nav_button(self, btn):
        btn.height = dp(80)
        btn.style = 'LabelNormalBold'
        btn.font_size = dp(8)
        btn.icon_font_size = dp(25)
        btn.content_padding = ['1dp', '0dp', '0dp', '0dp']
        btn.height_offset = dp(30)
        btn.font_color_tuple = ('Gray', '0000')
        btn._icon.height = dp(50)
        btn._label.height = dp(30)
        btn.radius = dp(15)

    def _create_navigation_button(self, entry):
        btn = entry.create_button(self._screenmanager)

        # Use for docked manager
        if self.use_dashboard_navigation:
            btn.theme = ('app', 'tabbarbutton')
            self._configure_docked_nav_button(btn)

        self._side_panel.spacing = dp(5)
        self._side_panel.padding = dp(5)

        self._side_panel.add_widget(btn)
        btn.bind(on_release=self._switch_to_screen)
        if len(self._screenmanager.children) == 0:
            self._screenmanager.add_widget(btn.config.screen)
        else:
            if not self.lazy_loading:
                self._screenmanager.add_widget(btn.config.screen)
        return btn

    def _switch_to_screen(self, instance, toggle_state=True):
        screen = instance.config.screen
        if screen not in self._screenmanager.screens:
            self._screenmanager.add_widget(screen)
        self._screenmanager.current = screen.name
        if toggle_state:
            self._navigationdrawer.toggle_state()

        if self.use_dashboard_navigation:
            for btn in self.nav_buttons:
                #btn.color_tuple = ('Gray', '300')
                btn.theme = ('app', 'tabbarbutton')
                self._configure_docked_nav_button(btn)
            instance.theme = ('app', 'tabbarbutton_highlighted')
            self._configure_docked_nav_button(instance)
            instance.color_tuple = (instance.color_tuple[0], '200')
            instance.icon_color_tuple = (instance.icon_color_tuple[0], '800')


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



