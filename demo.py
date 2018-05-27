
import sys
sys.path.append('flat_kivy_extensions/submodules')

#import os
#os.environ['KIVY_METRICS_DENSITY'] = '2.0'
#os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy .garden import garden_system_dir
print('Garden system dir: %s\n\n\n' % str(garden_system_dir))

from flat_kivy_extensions.flatappextension import ExtendedFlatApp, NavDrawerEntryConfig

# 1) Developer specifies application title and a string to describe
#    the application

title = 'My App Title'
about = 'Something to describe the purpose of the application.'

# 2) Developer specifies what screens should be included in
#    the screenmanger and how they should be referenced
#    in the navigation panel for switching

from screens import FlatKivyDemoScreen, KivyScreen1, KivyScreen2
from screens2 import (KivyWidgetScreen, CustomButtonDemoScreen,
                     CustomLayoutsScreen, DropShadowScreen, CustomSliderDemoScreen,
                     CustomCheckBoxDemoScreen)

from graph_screen import GraphDemoScreen
from pizza_screen import PizzaDemoScreen
from spinner_screen import SpinnerDemoScreen

from package_control_screen import PackageManagerScreen

#    An application configuration list is used to specify what screens
#    should be included and how to navigate to them.
#
#    This list  configures the widgets that are included in
#    the navigation side-panel. Eeach item in the list is used to configure
#    either a:
#
#     - Label used for navigation panel separator headers.  If
#       the item in the list is a string it is used as the text in a
#       navigation panel header.  If the item is a dict then
#       it is used as the kwargs when creating the FlatLabel for
#       a navigation panel header.
#
#     - NavigationDrawerEntry config each Screen to include.
#       Contsruction of a NavDrawerEntryConfig instance
#       requires at least a screen class, nd usually a string
#       that is used for navigation button title.  See xyz for details.
#

app_config_entries = ['Some Menu',
                      'Standard screens in app',
                      NavDrawerEntryConfig(SpinnerDemoScreen, 'SpinnerDemo'),
                      NavDrawerEntryConfig(PizzaDemoScreen, 'Pizza Demo'),
                      NavDrawerEntryConfig(KivyScreen1, 'Kivy Screen1'),
                      NavDrawerEntryConfig(KivyScreen2, 'Kivy Screen2'),
                      NavDrawerEntryConfig(FlatKivyDemoScreen, 'FlatKivy Demo'),
                      'Custom screens',
                      NavDrawerEntryConfig(KivyWidgetScreen, 'Kivy Widget Demo'),
                      NavDrawerEntryConfig(CustomButtonDemoScreen, 'Custom Buttons'),
                      NavDrawerEntryConfig(CustomCheckBoxDemoScreen, 'Custom CheckBoxes'),
                      NavDrawerEntryConfig(CustomSliderDemoScreen, 'Custom Sliders'),
                      'Special screens',
                      NavDrawerEntryConfig(GraphDemoScreen, 'Garden Graph Demo'),
                      NavDrawerEntryConfig(CustomLayoutsScreen, 'CustomLayouts'),
                      NavDrawerEntryConfig(DropShadowScreen, 'DropShadow Examples'),
                      #{'text':'Custom Heading Label',
                      # 'style':'Button',
                      # 'color_tuple' : ('Yellow', '500')},
                     ]

#
# Include themes or font stypes to override default application
# settings or add new ones
#
from app_themes_and_fonts import themes

if __name__ == '__main__':
    app = ExtendedFlatApp(app_config_entries, title, about, use_coverflow_navigation=True, themes=themes)
    app.run()

