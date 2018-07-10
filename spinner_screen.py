
import threading, time

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock, mainthread

from flat_kivy_extensions.uix.customscreen import CustomScreen
from kivy.garden.progressspinner import ProgressSpinner

Builder.load_string('''
<-SpinnerDemoScreen>:
    title: 'Spinner'
    theme: ('app', 'screen')

    ProgressSpinner:
        size_hint: (None, None)
        size: (dp(100), dp(100))
        color: 0.2, 0.3, .5, 1
        stroke_width: dp(5)
        stroke_length: 50.0
        speed: 1.2


    CustomButton:
        text: 'Show Progress Dialog'
        theme: ('app', 'default')
        size_hint: None, None
        size: dp(220), dp(50)
        on_release: root.start_process()

''')

class SpinnerDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(SpinnerDemoScreen, self).__init__(*largs, **kwargs)

        # self.spinner = ProgressSpinner()
        # self.spinner.size_hint = (None, None)
        # self.spinner.size = (dp(100),dp(100))
        # self.spinner.color = [0.2, 0.3, 0.4, 1.0]
        # #self.spinner.stroke_width = dp(16.5)
        # #self.spinner.stroke_length = 10
        # #self.spinner.speed = 2
        # self.add_widget(self.spinner)

        self.process_running = False

    def start_process(self, *largs):
        self.busy_popup = App.get_running_app().raise_busy('Currently Busy:', 'Some busy detail about what is going on...',
                                          auto_dismiss=False, timeout=2,
                                          timeout_callback=self.timeout,
                                          cancel_callback=self.canceled,)
        threading.Thread(target=self._threaded_process).start()

    def _threaded_process(self):
        self.process_running = True
        counter = 0
        while self.process_running:
            busy_text = 'Counter: %s' % str(counter)
            self.busy_popup.content.busy_text = busy_text
            time.sleep(1)
            counter += 1
        self.busy_popup.dismiss()

    #@mainthread
    #def _update_busy_text(self, *largs):
    #    print 'should update busy text to: %s' % str(self.busy_text)
    #    self.busy_content.busy_text = self.busy_text

    def show_error_dialog(self, *largs):
        App.get_running_app().raise_error('Some Error', 'Some error detail...',
                                          auto_dismiss=False)

    def timeout(self):
        print 'Error - something timed out'
        self.busy_popup.dismiss(animation=False)
        self.process_running = False
        Clock.schedule_once(self.show_timeout_error, 0.2)

    def show_timeout_error(self, *largs):
        message = '\n'.join(['Some detail about the error']*40)
        App.get_running_app().raise_error('Timeout Error', message, auto_dismiss=False)

    def canceled(self):
        print 'user canceled process'
        self.process_running = False

    #def on_enter(self, *largs):
    #    Clock.schedule_once(self.start_process)



