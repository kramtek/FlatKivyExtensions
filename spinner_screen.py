

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp

from flat_kivy_extensions.uix.customscreen import CustomScreen
from kivy.garden.progressspinner import ProgressSpinner

Builder.load_string('''
<-SpinnerDemoScreen>:
    title: 'Spinner'
    theme: ('app', 'screen')

    ProgressSpinner:
        size_hint: (None, None)
        size: (dp(100), dp(100))
        color: 0.2, 0.4, .2, 1
        stroke_width: dp(16.5)
        stroke_length: 10

    CustomButton:
        text: 'Show Something'
        theme: ('app', 'default')
        size_hint: None, None
        size: dp(200), dp(60)
        on_release: root.show_dialog()

''')

class SpinnerDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(SpinnerDemoScreen, self).__init__(*largs, **kwargs)

        # self.spinner = ProgressSpinner()
        # self.spinner.size_hint = (None, None)
        # self.spinner.size = (dp(100),dp(100))
        # self.spinner.color = [0.2, 0.3, 0.2, 1.0]
        # self.spinner.stroke_width = dp(16.5)
        # self.spinner.stroke_length = 10
        #self.spinner.speed = 2

        # self.add_widget(self.spinner)

    def show_dialog(self):
        App.get_running_app().raise_error('some error', 'Some detail...',
                                          auto_dismiss=False, timeout=20)



