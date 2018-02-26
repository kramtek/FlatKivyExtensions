
import sys
sys.path.append('flat_kivy_extensions/submodules')

from flat_kivy_extensions.flatappextension import ExtendedFlatApp

from flat_kivy_extensions.flatappextension import SomeScreen

app_config_entries = ['MainLabel',
                      ('Some Screen', SomeScreen, [], {}),
                     ]
title = 'My App Title'
about = 'Something to describe the purpose of the application.'

if __name__ == '__main__':
    ExtendedFlatApp(app_config_entries, title, about).run()
