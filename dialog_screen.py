
import threading, time

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock, mainthread

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.customdropdown import CustomDropDownButton
from kivy.garden.progressspinner import ProgressSpinner

Builder.load_string('''
<MyButton@CustomButton>:
    theme: ('app', 'default')
    size_hint: None, None
    size: dp(220), dp(40)

<-DialogDemoScreen>:
    title: 'Example Dialogs'
    theme: ('app', 'screen')
    content_spacing: dp(15)

    MyButton:
        text: 'Show Progress Dialog'
        on_release: root.start_background_process()

    MyButton:
        text: 'Show Error Dialog'
        on_release: root.show_error_dialog()

    MyButton:
        text: 'Show Long Dialog'
        on_release: root.show_long_dialog()

    MyButton:
        text: 'Show Busy in menu bar'
        on_release: root.show_busy_indicator()

    MyButton:
        text: 'Hide Busy in menu bar'
        on_release: root.hide_busy_indicator()

''')

class DialogDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(DialogDemoScreen, self).__init__(*largs, **kwargs)

        self.process_running = False

        self.strings = ['a', 'b', 'c', '123']
        self.dropdown_button = CustomDropDownButton(self.strings)
        # Set properties of main button
        self.dropdown_button.theme = ('app', 'default')
        self.dropdown_button.text = 'Select something'
        self.dropdown_button.size_hint = (None, None)
        self.dropdown_button.size = (dp(200), dp(40))
        self.dropdown_button.radius = 0
        # Set properties applied to all menu buttons
        self.dropdown_button.menubutton_theme = ('app', 'default')
        #self.dropdown_button.menubutton_color = (0.5, 0.5, 0.1, 0.6)

        self.dropdown_button.dropdown_width = dp(150)

        self.dropdown_button.bind(selected_item=self.menu_item_selected)
        self.add_widget(self.dropdown_button)

    def menu_item_selected(self, instance, index):
        print 'menu item selected:  text; %s' % str(self.strings[index])

    def start_background_process(self, *largs):
        self.busy_popup = App.get_running_app().raise_busy('Currently Busy:', '',
                                          auto_dismiss=False, timeout=5,
                                          timeout_callback=self.timeout,
                                          cancel_callback=self.canceled,)

        self.busy_popup.content.spinner_color=[.2, .2, .3, .9]
        threading.Thread(target=self._threaded_process).start()

    def _threaded_process(self):
        self.process_running = True
        counter = 0
        while self.process_running:
            self.busy_text = 'Counter: %s ' % str(counter)
            self.update_busy_text()
            time.sleep(1)
            counter += 1
        self.busy_popup.dismiss()

    @mainthread
    def update_busy_text(self):
        self.busy_popup.content.busy_text = self.busy_text

    def show_error_dialog(self, *largs):
        App.get_running_app().raise_error('Some Error', 'Some error detail...',
                                          auto_dismiss=False)

    def show_long_dialog(self, *largs):
        popup = App.get_running_app().raise_dialog('Some Information', ''.join(['Some error detail...']*40),
                                          auto_dismiss=False, okay_callback=self.allOkay)
        popup.content.message_alignment = 'right'

    def allOkay(self):
        print('Everything is okay..')

    def timeout(self):
        print 'Error - something timed out'
        self.busy_popup.dismiss(animation=False)
        self.process_running = False
        Clock.schedule_once(self.show_timeout_error, 0.2)

    def show_timeout_error(self, *largs):
        message = 'Some detail about the timeout error'
        App.get_running_app().raise_error('Timeout Error', message, auto_dismiss=False)

    def hide_busy_indicator(self, *largs):
        #App.get_running_app().show_busy_in_header(False)
        App.get_running_app().indicate_busy(False)

    def show_busy_indicator(self, *largs):
        #App.get_running_app().show_busy_in_header(True)
        App.get_running_app().indicate_busy(True)

    def canceled(self):
        print 'user canceled process'
        self.process_running = False




