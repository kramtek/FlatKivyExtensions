import sys
sys.path.append('flat_kivy_extensions/submodules')

#import os
#os.environ['KIVY_DPI'] = '2.0'
#os.environ['KIVY_METRICS_DENSITY'] = '2.0'
#os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy .garden import garden_system_dir
print('Garden system dir: %s\n\n\n' % str(garden_system_dir))

#from kivy.core.window import Window
#Window.rotation = 90

from flat_kivy_extensions.flatappextension import ExtendedFlatApp, NavDrawerEntryConfig

title = 'Garden Demos'
about = 'Demonstration of some kivy garden elements.'

from graph_screen import GardenGraphDemoScreen
from pizza_screen import PizzaDemoScreen
from spinner_screen import SpinnerDemoScreen
from package_control_screen import PackageManagerScreen
from code_review_screens import FileChooserScreen

app_config_entries = ['Garden Demos',
                      NavDrawerEntryConfig(GardenGraphDemoScreen, 'Garden Graph Demo'),
                      NavDrawerEntryConfig(SpinnerDemoScreen, 'SpinnerDemo'),
                      NavDrawerEntryConfig(FileChooserScreen, 'File Chooser'),
                      NavDrawerEntryConfig(PizzaDemoScreen, 'Pizza Demo'),
                      'Extra',
                      NavDrawerEntryConfig(PackageManagerScreen, 'Package Manager'),

                     ]

if __name__ == '__main__':
    app = ExtendedFlatApp(app_config_entries, title, about, use_coverflow_navigation=True)
    app.run()
