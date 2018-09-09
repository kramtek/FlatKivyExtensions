


from kivy.lang import Builder

from flat_kivy_extensions.flatappextension import CustomTabScreen, NavDrawerEntryConfig
from flat_kivy_extensions.uix.customscreen import CustomScreen


Builder.load_string('''
<-TabbedDemoScreen>:
    title: 'Shit'
    theme: ('app', 'screen')

    FlatLabel:
        text: 'test'
        color: (0,0,0,1)

<-SomeScreen1>:
    title: 'Screen 1'
    theme: ('app', 'screen')

    FlatLabel:
        text: 'screen #1'
        color: (0,0,0,1)

<-SomeScreen2>:
    title: 'Screen 2'
    theme: ('app', 'screen')

    FlatLabel:
        text: 'screen #2'
        color: (0,0,0,1)

<-SomeScreen3>:
    title: 'Screen 3'
    theme: ('app', 'screen')

    FlatLabel:
        text: 'screen #3'
        color: (0,0,0,1)

<-SomeScreen4>:
    title: 'Screen 4'
    theme: ('app', 'screen')

    FlatLabel:
        text: 'screen #4'
        color: (0,0,0,1)

''')



class TabDemoScreen(CustomTabScreen):

    def __init__(self, *largs, **kwargs):

        screen_config_entries = [
                                NavDrawerEntryConfig(SomeScreen1, 'Screen 1', button_icon='fa-gears'),
                                NavDrawerEntryConfig(SomeScreen2, 'Screen 2', button_icon='fa-comment-o'),
                                NavDrawerEntryConfig(SomeScreen3, 'Some Other Screen', button_icon='fa-gear'),
                                NavDrawerEntryConfig(SomeScreen4, 'Screen 4', button_icon='fa-wrench'),
                                ]

        super(TabDemoScreen, self).__init__(screen_config_entries, **kwargs)


class SomeScreen1(CustomScreen):
    pass

class SomeScreen2(CustomScreen):
    pass

class SomeScreen3(CustomScreen):
    pass

class SomeScreen4(CustomScreen):
    pass

