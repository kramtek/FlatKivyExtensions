
import sys
sys.path.append('flat_kivy_extensions/submodules')

from flat_kivy_extensions.flatappextension import ExtendedFlatApp

from screens import FlatKivyDemoScreen, KivyScreen1, KivyScreen2

app_config_entries = ['MainLabel',
                      ('FlatKivyDemo Screen', FlatKivyDemoScreen, [], {}),
                      'Sub Heading',
                      ('Kivy Screen 1', KivyScreen1, [], {}),
                      ('Kivy Screen 2', KivyScreen2, [], {}),
                     ]
title = 'My App Title'
about = 'Something to describe the purpose of the application.'

if __name__ == '__main__':
    ExtendedFlatApp(app_config_entries, title, about).run()
