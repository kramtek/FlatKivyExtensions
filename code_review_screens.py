



from kivy.metrics import dp
from kivy.lang import Builder

from flat_kivy_extensions.uix.customscreen import CustomScreen

Builder.load_string('''
<-FileChooserScreen>:
    title: 'File Editor'
    theme: ('app', 'screen')
    codeinput_layout: self.codeinput_layout
    filechooser_layout: self.filechooser_layout

    BoxLayout:
        id: filechooser_layout
        size_hint_y: None
        height: dp(400)
        canvas.before:
            Color:
                rgba: (0.1, 0.1, 0.1, 1.0)
            Rectangle:
                size: self.size
                pos: self.pos

        FileChooserListView:
            id: filechooser
            rootpath: './.'
            filters: ['*.py', '*.txt']

            #FileChooserListLayout:

    GridLayout:
        id: codeinput_layout
        cols: 1
        spacing: dp(5)
        orientation: 'vertical'
        size_hint_y: None
        height: dp(400)
        done_button: self.done_button

        CodeInput:
            id: codeinput
            padding: '4dp'
            text: 'class Hello(object):'
            # focus: True if root.parent else False
            focus: False
            font_size: dp(10)
            #disabled: True

        BoxLayout:
            size_hint_y: None
            height: dp(50)

            CustomButton:
                id: save_button
                theme: ('app', 'default')
                color_tuple: ('Red', '500')
                text: 'Save'
                size_hint_y: None
                height: dp(50)
                on_release: root.save_coding()
                disabled: True

            CustomButton:
                id: done_button
                theme: ('app', 'default')
                text: 'Done'
                size_hint_y: None
                height: dp(50)
                on_release: root.done_coding()

                on_parent: root.done_building()

''')

class FileChooserScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        self._built = False
        self._last_text = None
        super(FileChooserScreen, self).__init__(*largs, **kwargs)

    def done_building(self):
        if self._built:
            return
        self.filechooser = self.ids.filechooser
        self.filechooser_layout = self.ids.filechooser_layout
        self.codeinput_layout = self.ids.codeinput_layout
        self.codeinput = self.ids.codeinput
        self.done_button = self.ids.done_button
        self.save_button = self.ids.save_button

        self.filechooser.bind(selection=self.selection_updated)
        self.codeinput.bind(text=self.text_updated)
        self.remove_widget(self.codeinput_layout)

        self._built = True


    def selection_updated(self, filechooser, selection):
        print 'selection updated to: %s  ' % str(selection)

        self.add_widget(self.codeinput_layout)
        self.remove_widget(self.filechooser_layout)

        f = open(selection[0], 'r')
        lines = f.readlines()
        f.close()

        self._last_text = ''.join(lines)
        self.codeinput.text = self._last_text
        self.selection = selection[0]
        self.save_button.disabled = True

    def text_updated(self, instance, text):
        if self._last_text == text:
            return
        self.save_button.disabled = False
        self._last_text = text

    def save_coding(self):
        f = open(self.selection, 'w')
        f.writelines(self._last_text.strip()+'\n')
        f.close()

    def done_coding(self):
        self.add_widget(self.filechooser_layout)
        self.remove_widget(self.codeinput_layout)
        return
        self.codeinput_layout.size_hint = (None, None)
        self.codeinput_layout.size = (0,0)
        #self.done_button.height = 0
        self.codeinput_layout.remove_widget(self.done_button)

        self.filechooser_layout.size_hint=(None, None)
        self.filechooser_layout.height = self.height-dp(40)
        self.filechooser_layout.width= self.width
        self.filechooser.size_hint=(None, None)
        self.filechooser.height = self.height-dp(40)
        self.filechooser.width= self.width



