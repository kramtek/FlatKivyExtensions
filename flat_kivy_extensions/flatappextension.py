import time, threading

from navigationscreen import NavigationScreen

from kivy.clock import mainthread
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
from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.thumbnailwidget import ThumbNailWidget

import os
import flat_kivy
flat_kivy_font_path = os.path.join(os.path.dirname(os.path.abspath(flat_kivy.__file__)), *['data', 'font'])
import flat_kivy_extensions
extensions_font_path = os.path.join(os.path.dirname(os.path.abspath(flat_kivy_extensions.__file__)), *['data', 'font'])

paths = [flat_kivy_font_path, extensions_font_path]
common_prefix = os.path.commonprefix(paths)
relative_paths = [os.path.relpath(path, common_prefix) for path in paths]
components = relative_paths[0].split(os.sep)
relative_path_to_extensions  = os.sep.join(['..']*len(components))
relative_path_to_fonts  = os.path.join(relative_path_to_extensions, relative_paths[1])

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

                ScreenManager:
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

''')


Builder.load_file('flat_kivy_extensions/ui_elements.kv')

class HeaderLayout(BoxLayout):
    pass

class RootWidget(Widget):
    pass


class ExtendedFlatApp(FlatApp):
    def __init__(self, app_config_entries, title, about, *largs, **kwargs):
        super(ExtendedFlatApp, self).__init__(*largs, **kwargs)
        self.title = title
        self.app_config_entries = app_config_entries
        self.about = about
        self.lazy_loading = False
        self.use_coverflow_navigation = kwargs.get('use_coverflow_navigation', False)
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


        entry_constructors = {type(str()) : self._create_navigation_label_from_string,
                              type(dict()) : self._create_navigation_label_from_dict,
                              type(tuple()) : self._create_navigation_button,
                              }

        for entry in self.app_config_entries:
            entry_constructors[type(entry)](entry)

        if not self.use_coverflow_navigation:
            return self.root

        self._thumbnails = list()
        self._is_opening = True
        self._open_screen_index = len(self._screenmanager.screens)-1
        self.open_all_screens()

        return self.root

    @mainthread
    def open_all_screens(self):
        screen = self._screenmanager.screens[self._open_screen_index]
        screen.bind(on_enter=self._local_on_enter)
        self._screenmanager.current = screen.name

    def _local_on_touch_up(self, touch):
        print 'local on touch up for thumbnail...'

    def _local_on_enter(self, screen):
        #screen.on_enter(screen)
        if not self._is_opening:
            return
        thumbnail = ThumbNailWidget(screen)
        thumbnail.bind(on_touch_up=self._local_on_touch_up)
        self._thumbnails.append((thumbnail, screen.name))
        self._open_screen_index -= 1
        if self._open_screen_index >= 0:
            self.open_all_screens()
        else:
            self.finalize()

    @mainthread
    def finalize(self):
        entry = ('Navigation Screen', NavigationScreen, [self._thumbnails], {})
        self._create_navigation_button(entry)
        self._screenmanager.current = self._screenmanager.screens[-1].name
        #self._screenmanager.current = self._screenmanager.screens[0].name
        self._is_opening = False
        self._screenmanager.transition = FadeTransition()

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
                },
            'CustomSliderTouchRippleBehavior' : {
            },

            'CustomSlider': {
                'color_tuple' : ('Brown', '600'),
                'outline_color_tuple' : ('Brown', '700'),
                'slider_color_tuple' : ('Blue', '200'),
                'slider_outline_color_tuple' : ('Green', '700'),
                'ripple_color_tuple' : ('Brown', '400'),
                },
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
                'green' : {'main' : main,
                           'accent' : accent,
                           }
                 }
        self.add_themes(themes)

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
        }

        screen = {
            'FlatLabel': {
                'color_tuple' : ('Brown', '800'),
                'style' : 'HeaderTitle',
                'size_hint_y' : None,
                'height' : '40dp',
             },
        }

        grouped_layout = {
            'FlatLabel': {
                'color_tuple': ('Orange', '800'),
                'style': 'GroupedLayoutTitle',
                'size_hint_y': None,
                'height': '35dp',
            },
        }

        default = {
            'CustomButton': {
               'color_tuple': ('Brown', '500'),
                'font_color_tuple': ('Gray', '100'),
                'style': 'CustomButton1',
                'radius' : '10dp',
            },
            'CustomCheckBoxListItem': {
                'font_color_tuple': ('Blue', '800'),
                'check_color_tuple': ('Green', '600'),
                'check_color_hue_down': '200',
                'outline_color_tuple': ('Gray', '500'),
                'style': 'Button',
                'valign' : 'middle',

                'size_scaling' : 0.6,
                'outline_size': '1.5dp',
                'style': 'CustomButton1',

                'check_scale': .6,
                'radius' : '4dp',
                'icon' : 'fa-check',
            },

        }


        themes = {
                'app' : {'header' : header,
                         'navigationdrawer' : navigationdrawer,
                         'screen' : screen,
                         'grouped_layout' : grouped_layout,
                         'default' : default,
                        }
                }

        #self.theme_manager.add_theme('green', 'main', main)
        #self.theme_manager.add_theme('green', 'accent', accent)

        #self.theme_manager.add_theme('app', 'header', header)
        #self.theme_manager.add_theme('app', 'navigationdrawer', navigationdrawer)
        #self.theme_manager.add_theme('app', 'screen', screen)
        #self.theme_manager.add_theme('app', 'grouped_layout', grouped_layout)
        #self.theme_manager.add_theme('app', 'default', default)

        self.add_themes(themes)

        from flat_kivy_extensions.uix.custombutton import CustomButton
        from flat_kivy_extensions.uix.customslider import CustomSlider, CustomSliderTouchRippleBehavior
        from flat_kivy_extensions.uix.customcheckbox import CustomCheckBoxListItem
        self.theme_manager.types_to_theme['CustomSlider'] = CustomSlider
        self.theme_manager.types_to_theme['CustomSliderTouchRippleBehavior'] = CustomSliderTouchRippleBehavior
        self.theme_manager.types_to_theme['CustomButton'] = CustomButton
        self.theme_manager.types_to_theme['CustomIconButton'] = CustomIconButton
        self.theme_manager.types_to_theme['CustomCheckBoxListItem'] = CustomCheckBoxListItem
        self.theme_manager.types_to_theme['FlatIconButtonLeft'] = FlatIconButtonLeft

    def add_themes(self, themes):
        for (theme, value) in themes.items():
            for (variant, theme_dict) in value.items():
                self.theme_manager.add_theme(theme, variant, theme_dict)


    def setup_font_ramps(self):
        super(ExtendedFlatApp, self).setup_font_ramps()

        font_styles = {
            'HeaderTitle': {
                #'font': 'Roboto-Bold.ttf',
                # Question: what is the best way to include additional fonts?
                'font': '%s/proximanova-regular-webfont.ttf' % relative_path_to_fonts,
                'sizings': {'mobile': (25, 'sp'), 'desktop': (20, 'sp')},
                'alpha': .87,
                'wrap': False,
                },
            'NavigationButton': {
                #'font': 'Roboto-Bold.ttf',
                'font': '%s/proximanova-regular-webfont.ttf' % relative_path_to_fonts,
                'sizings': {'mobile': (16, 'sp'), 'desktop': (14, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            'NavigationLabelMainHeading': {
                #'font': 'Roboto-Bold.ttf',
                'font': '%s/proximanova-bold-webfont.ttf' % relative_path_to_fonts,
                'sizings': {'mobile': (20, 'sp'), 'desktop': (17, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            'NavigationLabelSubHeading': {
                #'font': 'Roboto-Bold.ttf',
                'font': '%s/proximanova-bold-webfont.ttf' % relative_path_to_fonts,
                'sizings': {'mobile': (18, 'sp'), 'desktop': (15, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            'GroupedLayoutTitle': {
                #'font': 'Roboto-Bold.ttf',
                'font': '%s/proximanova-bold-webfont.ttf' % relative_path_to_fonts,
                'sizings': {'mobile': (22, 'sp'), 'desktop': (17, 'sp')},
                'alpha': .87,
                'wrap': False,
            },
            'CustomButton1': {
                #'font': 'Roboto-Bold.ttf',
                'font': '%s/proximanova-semibold-webfont.ttf' % relative_path_to_fonts,
                'sizings': {'mobile': (17, 'sp'), 'desktop': (17, 'sp')},
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

    def _create_navigation_label_from_string(self, entry):
        entry = {'text' : entry, 'theme' : ('app', 'navigationdrawer')}
        if self._first_navigation_label is None:
            self._first_navigation_label = self._create_navigation_label_from_dict(entry)
            return
        entry['style'] = 'NavigationLabelSubHeading'
        self._create_navigation_label_from_dict(entry)

    def _create_navigation_label_from_dict(self, entry):
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
        btnText = entry[0]
        btn = FlatIconButtonLeft(text=btnText)
        btn.theme = ('app', 'navigationdrawer')

        # Question: best way to set these? should something be
        #           customized, e.g. NavigationIconButton(FlatIconButtonLeft),
        #           such that the properties are forwarded or
        #           is it okay to do it here like this?
        btn.ids.icon.font_size = '15dp'
        btn.ids.label.halign = 'left'

        self._side_panel.add_widget(btn)

        btn.config = entry
        btn.screen = None
        btn.bind(on_release=self._switch_to_screen)

        if self._first_screen is None:
            self._first_screen = self._create_screen(btn)

        if not self.lazy_loading:
            self._create_screen(btn)

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
        if instance.screen is None:
            self._create_screen(instance)
        self._screenmanager.current = instance.screen.name
        self._navigationdrawer.toggle_state()


