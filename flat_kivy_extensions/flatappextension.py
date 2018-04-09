
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, FadeTransition, NoTransition

from flat_kivy.flatapp import FlatApp
from flat_kivy.uix.flattextinput import FlatTextInput
from flat_kivy.uix.flaticonbutton import FlatIconButtonLeft
from flat_kivy.uix.flatlabel import FlatLabel
from flat_kivy.font_definitions import style_manager

from flat_kivy_extensions.uix.customiconbutton import CustomIconButton

Builder.load_string('''
#:import NavigationDrawer kivy_garden.navigationdrawer.NavigationDrawer
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

                ScreenManager:
                    id: screenmanager
                    transition: NoTransition()
                    # Question: When selecting FadeTransition the switching
                    #           annimation seems to go black when switching,
                    #           how can this be avoided?
                    transition: FadeTransition()
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

''')


Builder.load_file('flat_kivy_extensions/ui_elements.kv')

class HeaderLayout(BoxLayout):
    pass

class RootWidget(Widget):
    pass

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
    def __init__(self, app_config_entries, title, about, *largs, **kwargs):
        super(ExtendedFlatApp, self).__init__(*largs, **kwargs)
        self.title = title
        self.app_config_entries = app_config_entries
        self.about = about
        self.lazy_loading = False
        self._first_screen = None
        self._first_navigation_label = None

    def build(self):
        self.root = RootWidget()
        # Question: Is this the best place to get references to
        #           widgets with ids in the root widget?
        self._navigationdrawer = self.root.ids.navigationdrawer
        self._side_panel = self.root.ids.side_panel
        self._header = self.root.ids.header
        self._screenmanager = self.root.ids.screenmanager
        self._menu_button = self._header.ids._menu_button
        self._menu_button.bind(on_press=lambda j: self._navigationdrawer.toggle_state())


        #entry_constructors = {type(str()) : self._create_navigation_label_from_string,
        #                      type(dict()) : self._create_navigation_label_from_dict,
        #                      type(tuple()) : self._create_navigation_button,
        #                      }
#
#        for entry in self.app_config_entries:
#            entry_constructors[type(entry)](entry)

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


        themes = {
                  'green': {'main': main,
                  'accent': accent,
                  }
                }
#        self.theme_manager.add_theme('green', 'main', main)
#        self.theme_manager.add_theme('green', 'accent', accent)
        self.add_themes(themes, {})

        header = {
            'CustomIconButton': {
                'color_tuple': ('Brown', '900'),
                'font_color_tuple': ('Gray', '100'),
                'style': 'Button',
                'icon_color_tuple': ('Gray', '100'),
                'icon_font_size' : '25dp',
                },
            'FlatLabel': {
                'color_tuple' : ('Orange', '500'),
                'style' : 'HeaderTitle',
                },
            }

        navigationdrawer = {
            'FlatLabel': {
                'size_hint_y' : None,
                'height' : '35dp',
                # 'font_size' : '20dp',
                'color_tuple' : ('Green', '300'),
                'style' : 'NavigationLabelMainHeading',
            },
            'FlatIconButtonLeft': {
                'color_tuple': ('Brown', '800'),
                'font_color_tuple': ('Blue', '300'),
                'size_hint_y' : None,
                'height' : '35dp',
                'icon' : 'fa-chevron-right',
                'icon_color_tuple': ('Red', '500'),
                'padding' : '3dp',
                'style': 'NavigationButton',
            },
            'CustomIconButton': {
                'color_tuple': ('Brown', '800'),
                'font_color_tuple': ('Blue', '300'),
                'size_hint_y' : None,
                'height' : '35dp',
                'icon' : 'fa-chevron-right',
                'icon_color_tuple': ('Red', '500'),
                'icon_font_size' : '15dp',
                'content_padding' : ['3dp', '2dp', '2dp', '0dp'],
                'style': 'NavigationButton',
                'orientation' : 'tb-rl',
            },
        }

        themes = {
            'app' : {'header' : header,
                 'navigationdrawer' : navigationdrawer,
                 }
            }

        #self.theme_manager.add_theme('app', 'header', header)
        #self.theme_manager.add_theme('app', 'navigationdrawer', navigationdrawer)

        types_to_theme = {
            'CustomIconButton' : CustomIconButton,
            'FlatIconButtonLeft' : FlatIconButtonLeft,
            }
        self.add_themes(themes, types_to_theme)

        #self.theme_manager.types_to_theme['CustomIconButton'] = CustomIconButton
        #self.theme_manager.types_to_theme['FlatIconButtonLeft'] = FlatIconButtonLeft

    def add_themes(self, themes, types_to_theme={}):
        for (theme, value) in themes.items():
            for (variant, theme_dict) in value.items():
                self.theme_manager.add_theme(theme, variant, theme_dict)
        for (key,value) in types_to_theme.items():
            self.theme_manager.types_to_theme[key] = value


    def setup_font_ramps(self):
        super(ExtendedFlatApp, self).setup_font_ramps()

        font_styles = {
            'HeaderTitle': {
                'font': 'Roboto-Bold.ttf',
                # Question: what is the best way to include additional fonts?
                #'font': 'proximanova-bold-webfont.ttf',
                'sizings': {'mobile': (25, 'sp'), 'desktop': (20, 'sp')},
                'alpha': .87,
                'wrap': False,
                },
            'NavigationButton': {
                'font': 'Roboto-Bold.ttf',
                # 'font': 'proximanova-bold-webfont.ttf',
                'sizings': {'mobile': (16, 'sp'), 'desktop': (14, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            'NavigationLabelMainHeading': {
                'font': 'Roboto-Bold.ttf',
                # 'font': 'proximanova-bold-webfont.ttf',
                'sizings': {'mobile': (20, 'sp'), 'desktop': (17, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            'NavigationLabelSubHeading': {
                'font': 'Roboto-Bold.ttf',
                # 'font': 'proximanova-bold-webfont.ttf',
                'sizings': {'mobile': (18, 'sp'), 'desktop': (15, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            }
        self.add_font_styles(font_styles)

    def add_font_styles(self, font_styles):
        for each in font_styles:
            style = font_styles[each]
            sizings = style['sizings']
            style_manager.add_style(style['font'], each, sizings['mobile'],
                sizings['desktop'], style['alpha'])

#    def _create_navigation_label_from_string(self, entry):
#        entry = {'text' : entry, 'theme' : ('app', 'navigationdrawer')}
#        if self._first_navigation_label is None:
#            self._first_navigation_label = self._create_navigation_label_from_dict(entry)
#            return
#        entry['style'] = 'NavigationLabelSubHeading'
#        self._create_navigation_label_from_dict(entry)

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

#         btnText = entry[0]
#         btn = FlatIconButtonLeft(text=btnText)
#         btn.theme = ('app', 'navigationdrawer')
#
#         # Question: best way to set these? should something be
#         #           customized, e.g. NavigationIconButton(FlatIconButtonLeft),
#         #           such that the properties are forwarded or
#         #           is it okay to do it here like this?
#         btn.ids.icon.font_size = '15dp'
#         btn.ids.label.halign = 'left'
#
#         self._side_panel.add_widget(btn)
#
#         btn.config = entry
#         btn.screen = None
#         btn.bind(on_release=self._switch_to_screen)
#
#         if self._first_screen is None:
#             self._first_screen = self._create_screen(btn)
#
#         if not self.lazy_loading:
#             self._create_screen(btn)

    def _create_screen(self, button):
        if button.screen is None:
            print('Creating instance: screen = ' +
                  str(button.config[1].__name__ +
                      "(*" + str(button.config[2]) +
                      ", **" + str(button.config[3]) + ')'))
            button.screen = button.config[1](*button.config[2], **button.config[3])
            button.screen.name = button.config[0]
            self._screenmanager.add_widget(button.screen)
            return button.screen

    def _switch_to_screen(self, instance):
        screen = instance.config.screen
        print 'switching to screen: %s'  % str(screen)
        if screen not in self._screenmanager.screens:
            self._screenmanager.add_widget(screen)
        self._screenmanager.current = screen.name
        self._navigationdrawer.toggle_state()

#        if instance.screen is None:
#            self._create_screen(instance)
#        self._screenmanager.current = instance.screen.name
#        self._navigationdrawer.toggle_state()


