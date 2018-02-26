
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

Builder.load_string('''
<-FlatKivyDemoScreen>:
    BoxLayout:
        orientation: 'vertical'

        OriginalFlatKivyDemoLayout:

<-OriginalFlatKivyDemoLayout>:
    orientation: 'vertical'

    GridLayout:
        cols: 3
        pos: root.pos
        size: root.size
        padding: '5dp'
        spacing: '5dp'
        canvas.before:
            Color:
                rgb: 1,1,1
            Rectangle:
                pos: self.pos
                size: self.size

        FlatButton:
            text: 'button'
            theme: ('green', 'accent')

        FlatIconButton:
            text: 'icon button'
            icon: 'fa-tree'
            theme: ('green', 'accent')

        FlatToggleButton:
            text: 'toggle button'
            group: 'toggle'
            theme: ('green', 'accent')

        RaisedFlatToggleButton:
            text: 'raised toggle button'
            group: 'toggle'
            theme: ('green', 'accent')

        FlatCheckBoxListItem:
            text: 'check 1'
            group: 'check'
            theme: ('green', 'accent')

        FlatCheckBoxListItem:
            text: 'check 2'
            group: 'check'
            theme: ('green', 'accent')

        FlatCard:
            image_source: 'flat_kivy/AstroPic1.jpg'
            text: 'the card'
            color_tuple: ('Gray', '0000')

        FlatTextInput:

        BoxLayout:
            orientation: 'vertical'
            FlatLabel:
                text: 'FlatScrollView'
                size_hint_y: None
                height: '35dp'
                theme: ('green', 'main')

            FlatScrollView:
                do_scroll_x: False

                BoxLayout:
                    orientation: 'vertical'
                    height: '400dp'
                    size_hint_y: None
                    FlatLabel:
                        text: '1'
                    FlatLabel:
                        text: '2'
                    FlatLabel:
                        text: '3'
                    FlatLabel:
                        text: '4'
                    FlatLabel:
                        text: '5'
                    FlatLabel:
                        text: '6'

        RaisedFlatButton:
            text: 'popup'
            theme: ('green', 'accent')
            on_release: popup_demo.open()
            popup_demo: popup_demo.__self__

        FlatPopup:
            id: popup_demo
            title: 'Flat Popup Demo'
            size_hint: .6,.6
            on_parent: if self.parent: self.parent.remove_widget(self)

            BoxLayout:
                spacing: '5dp'
                padding: '5dp'
                RaisedFlatButton:
                    text: 'just a button in here'
                    theme: ('green', 'main')
                RaisedFlatButton:
                    text: 'just a button in here'
                    theme: ('green', 'main')

        FlatSlider:
            id: hor_slider
            orientation: 'horizontal'
            min: 10
            value: ver_slider.value
            theme: ('green', 'main')

        FlatSlider:
            id: ver_slider
            orientation: 'vertical'
            min: 10
            value: hor_slider.value
            theme: ('green', 'main')

        FlatSlider:
            value: hor_slider.value
            orientation: 'horizontal'
            disabled: True
            theme: ('green', 'main')


''')

class FlatKivyDemoScreen(Screen):
    pass

class OriginalFlatKivyDemoLayout(BoxLayout):
    pass


Builder.load_string('''
<-KivyScreen1>:

    BoxLayout:
        id: container
        orientation: 'vertical'

        Button:
            text: 'button'

        Label:
            text: 'label'
            color: (.1, .1, .1)

''')


class KivyScreen1(Screen):
    pass


class KivyScreen2(Screen):

    def __init__(self, *largs, **kwargs):
        super(KivyScreen2, self).__init__(*largs, **kwargs)

        container = BoxLayout(orientation='vertical')

        label = Label(text='label')
        label.color = (.1, .1, .1)

        button = Button(text='button')

        container.add_widget(label)
        container.add_widget(button)

        self.add_widget(container)




