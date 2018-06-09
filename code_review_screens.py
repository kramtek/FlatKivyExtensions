

import difflib

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder

from flat_kivy_extensions.uix.customscreen import CustomScreen

Builder.load_string('''
<-FileChooserScreen>:
    title: 'File Editor'
    theme: ('app', 'screen')
    codeinput_layout: codeinput_layout.__self__
    filechooser_layout: filechooser_layout.__self__

    BoxLayout:
        id: filechooser_layout
        size_hint_y: None
        height: root.container_height
        canvas.before:
            Color:
                rgba: (0.1, 0.2, 0.1, 1.0)
            Rectangle:
                size: self.size
                pos: self.pos

        FileChooserListView:
            id: filechooser
            rootpath: './.'
            filters: ['*.py', '*.txt']
            #size_hint_y: None
            #height: root.container_height

            #FileChooserListLayout:

    GridLayout:
        id: codeinput_layout
        cols: 1
        spacing: dp(5)
        orientation: 'vertical'
        #size_hint_y: None
        #height: dp(400)
        done_button: self.done_button

        CustomButton:
            id: keyboard_button
            theme: ('app', 'default')
            size_hint_y: None
            height: dp(20)
            text: 'Show Keyboard'
            color_tuple: ('Gray', '600')
            font_size: dp(12)
            radius: dp(2)
            on_release: root.show_keyboard()

        CodeInput:
            id: codeinput
            padding: '4dp'
            size_hint_y: None
            height: root.container_height - dp(20+50)
            multiline: True
            text: 'class Hello(object):'
            # focus: True if root.parent else False
            focus: False
            font_size: dp(10)
            #disabled: True
            keyboard_mode: 'managed'
            #on_parent: self.hide_keyboard
            #on_double_tap: root.double_tap
            #on_text_validate: root.validate_text()

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(5)

            CustomButton:
                id: save_button
                theme: ('app', 'default')
                color_tuple: ('Gray', '200')
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
        self.keyboard_button = self.ids.keyboard_button

        self.filechooser.bind(selection=self.selection_updated)
        self.codeinput.bind(text=self.text_updated)
        self.codeinput.bind(on_double_tap=self.double_tap)
        self.codeinput.bind(on_text_validate=self.validate_text)
        self.remove_widget(self.codeinput_layout)

        #self.filechooser_layout.size_hint_y = None
        #self.filechooser_layout.height = self.container_height

        #self.filechooser.size_hint_y = None
        #self.filechooser.height = self.filechooser_layout.height


        self._built = True
        self._keyboard_open = False

    def selection_updated(self, filechooser, selection):
        print 'selection updated to: %s  ' % str(selection)

        self.add_widget(self.codeinput_layout)
        self.remove_widget(self.filechooser_layout)

        f = open(selection[0], 'r')
        lines = f.readlines()
        f.close()

        self.codeinput.text = ''
        self._last_text = ''.join(lines)
        self.codeinput.text = self._last_text
        self.selection = selection[0]
        self.save_button.disabled = True
        self.save_button.color_tuple = ('Gray', '200')

    def _keyboard_closed(self):
        print 'keyboard_closed'
        if not self._keyboard_open:
            self.codeinput.show_keyboard()
            return
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def validate_text(self, *largs):
        print 'validating text...'

    def show_keyboard(self, *largs):
        if self._keyboard_open:
            self.codeinput.hide_keyboard()
            self.codeinput.height = self.container_height - dp(20+50)
        else:
            self.codeinput.show_keyboard()
            self.codeinput.height = self.container_height / 2.0
            #self._keyboard = Window.request_keyboard(
            #    self._keyboard_closed, self)
            #self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard_open = not self._keyboard_open
        self.keyboard_button.text = 'Show Keyboard' if not self._keyboard_open else 'Hide Keyboard'

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print str(keycode)
        #if keycode[1] == 'enter':
        #    return True
        return False


    def double_tap(self, *largs):
        print 'double tap'
        self.show_keyboard()

    def text_updated(self, instance, text):
        if self._last_text == text:
            return

        if self._last_text is not None:
        #    h = ''.join(difflib.ndiff(self._last_text, text))
        #    print 'diff: "%s"' % str(h)
            seqm = difflib.SequenceMatcher(None, self._last_text, text)
            for (opcode, a0, a1, b0, b1) in seqm.get_opcodes():
                if opcode == 'insert':
                    if seqm.b[b0:b1] == '\n':
                        print ' we know that keyboard is going away... but why?'
                        #def show_it(*largs):
                        #    print '  really reshowing keyboard?'
                        #    self.codeinput.focus = True
                        #    self.codeinput.show_keyboard()
                        #Clock.schedule_once(show_it)
                        self.show_keyboard()

        self.save_button.disabled = False
        self.save_button.color_tuple = ('Red', '500')
        self._last_text = text

    def save_coding(self):
        f = open(self.selection, 'w')
        f.writelines(self._last_text.strip()+'\n')
        f.close()
        self.save_button.disabled = True
        self.save_button.color_tuple = ('Gray', '200')

    def done_coding(self):
        self.add_widget(self.filechooser_layout)
        self.remove_widget(self.codeinput_layout)



