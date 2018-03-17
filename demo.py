
import sys
sys.path.append('flat_kivy_extensions/submodules')

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

#    An application configuration list is used to specify what screens
#    should be included and how to navigate to them.
#
#    This configuration list defines the widgets that are included in
#    the navigation side-panel and each item in the list is used to configure
#    either a:
#
#     - Label used for navigation panel separator headers
#
#     - Button for each Screen to include.
#         Each button instance holds a reference to the screen
#         and triggers navigation to that screen via on_release

# Each item in the app_config_entries list must be one of the following types:
#
#  str():  Text used in a Label that is added to th navigation slide-out panel
#
#  dict(): Dict of configuration properties that is used to construct
#          a Label that is added to the navigation slide out-panel
#
#  instance of NavDrawerEntryConfig.
#           instantiating a NavDrawerEntryConfig requires at least
#           a screen class.
#

app_config_entries = ['Demo Option',
                      'Standard screens in app',
                      NavDrawerEntryConfig(KivyScreen1, 'Kivy Screen1'),
                      NavDrawerEntryConfig(KivyScreen2, 'Kivy Screen2'),
                      NavDrawerEntryConfig(FlatKivyDemoScreen, 'FlatKivy Demo'),
                      'Custom screens',
                      NavDrawerEntryConfig(KivyWidgetScreen, 'Kivy Widget Demo'),
                      NavDrawerEntryConfig(CustomButtonDemoScreen, 'Custom Buttons'),
                      NavDrawerEntryConfig(CustomSliderDemoScreen, 'Custom Sliders'),
                      NavDrawerEntryConfig(GraphDemoScreen, 'Garden Graph Demo'),
                      NavDrawerEntryConfig(CustomLayoutsScreen, 'CustomLayouts'),
                      NavDrawerEntryConfig(DropShadowScreen, 'DropShadow Examples'),
                      {'text':'Custom Heading Label',
                       'style':'Button',
                       'color_tuple' : ('Yellow', '500')},
                     ]

if __name__ == '__main__':
    app = ExtendedFlatApp(app_config_entries, title, about, use_coverflow_navigation=True)
    app.run()
