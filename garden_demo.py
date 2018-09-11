
#import os
#os.environ['KIVY_DPI'] = '2.0'
#os.environ['KIVY_METRICS_DENSITY'] = '2.0'
#os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy .garden import garden_system_dir
print('Garden system dir: %s\n\n\n' % str(garden_system_dir))

#from kivy.core.window import Window
#Window.rotation = 90

from flat_kivy_extensions.flatappextension import ExtendedFlatApp, ScreenNavigationEntry


from flat_kivy_extensions.uix.customicon import CustomIcon

title = 'Garden Demos'
about = 'Demonstration of some kivy garden elements.'

from graph_screen import GardenGraphDemoScreen
from pizza_screen import PizzaDemoScreen
from spinner_screen import SpinnerDemoScreen
from package_control_screen import PackageManagerScreen
from flat_kivy_extensions.screens.file_edit_screen import FileEditScreen

from icon_screen import IconDemoScreen

app_config_entries = ['Garden Demos',
                      ScreenNavigationEntry(IconDemoScreen, 'Icons...', screen_kwargs={'use_scrollview' : True}),
                      ScreenNavigationEntry(SpinnerDemoScreen, 'SpinnerDemo'),
                      ScreenNavigationEntry(GardenGraphDemoScreen, 'Garden Graph Demo'),
                      ScreenNavigationEntry(FileEditScreen, 'File Chooser'),
                      ScreenNavigationEntry(PizzaDemoScreen, 'Pizza Demo'),
                      'Extra',
                      ScreenNavigationEntry(PackageManagerScreen, 'Package Manager'),

                     ]

if __name__ == '__main__':
    app = ExtendedFlatApp(app_config_entries, title, about, use_coverflow_navigation=True)
    app.run()
