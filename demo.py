
import sys
sys.path.append('flat_kivy_extensions/submodules')

from flat_kivy_extensions.flatappextension import ExtendedFlatApp

# 1) Developer specifies application title and a string to describe
#    the application

title = 'My App Title'
about = 'Something to describe the purpose of the application.'

# 2) Developer specifies what screens should be included in
#    the screenmanger and how they should be referenced
#    in the navigation panel for switching

from screens import FlatKivyDemoScreen, KivyScreen1, KivyScreen2
from screens2 import CustomScreen1, CustomScreen2, CustomScreen3, CustomScreen4
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
#  tuple(): [0] string defining the text property of the navigation button,
#           [1] class name of screen to construct and link button to
#           [2] *largs that are passed to screen constructor
#           [3] **kwargs that are passed to screen constructor
#

app_config_entries = ['Main Label',
                      ('Custom Widgets', CustomScreen2, [], {}),
                      ('Custom Screen Example', CustomScreen1, [], {}),
                      ('Grouped Layouts', CustomScreen3, [], {}),
                      ('Drop Shadowed Widgets', CustomScreen4, [], {}),

                      ('FlatKivyDemo Screen', FlatKivyDemoScreen, [], {}),
                      'SubHeading Label',
                      ('Kivy Screen 1', KivyScreen1, [], {}),
                      ('Kivy Screen 2', KivyScreen2, [], {}),
                      {'text':'Custom Heading Label',
                       'style':'NavigationLabelSubHeading',
                       'color_tuple' : ('Yellow', '500')},

                     ]

if __name__ == '__main__':
    ExtendedFlatApp(app_config_entries, title, about).run()
