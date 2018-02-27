
import sys
sys.path.append('flat_kivy_extensions/submodules')

from flat_kivy_extensions.flatappextension import ExtendedFlatApp

from screens import FlatKivyDemoScreen, KivyScreen1, KivyScreen2

# Each item in the app_config_entries list must be one of the following:
#
#  str():  Label text that should be placed in navigation slide out panel
#
#  dict(): Label configuration properties that can be used to construct
#          the navigation label for customization
#
#  tuple(): [0] indicating the text that is applied to the navigation button,
#           [1] class name of screen to link to
#           [2] *largs that are passed to screen constructor
#           [3] **kwargs that are passed to screen constructor
#
app_config_entries = ['Main Label',
                      ('FlatKivyDemo Screen', FlatKivyDemoScreen, [], {}),
                      'SubHeading Label',
                      ('Kivy Screen 1', KivyScreen1, [], {}),
                      ('Kivy Screen 2', KivyScreen2, [], {}),
                      {'text':'Custom Heading Label', 'style':'NavigationLabelSubHeading', 'color_tuple' : ('Yellow', '500')},
                     ]
title = 'My App Title'
about = 'Something to describe the purpose of the application.'

if __name__ == '__main__':
    ExtendedFlatApp(app_config_entries, title, about).run()
