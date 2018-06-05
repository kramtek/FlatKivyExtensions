
import threading, time
import numpy as np

from flat_kivy_extensions.uix.customscreen import CustomScreen
from flat_kivy_extensions.uix.custombutton import CustomButton
from kivy.garden.pizza import Pizza

from kivy.metrics import dp
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<-PizzaDemoScreen>:
    title: 'Pie Chart'
    theme: ('app', 'screen')
''')

class PizzaDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(PizzaDemoScreen, self).__init__(*largs, **kwargs)

        self.running = False

        self.labels = ["SpQ", "SpN", "InCar", "RevSp", "Noise", 'Music']
        self.values = np.ones(6, dtype=np.float32) * (100.0/6)
        self.colors = ['a9a9a9', '808080', '696969', '778899', '708090', '608090']

        self.pizza = Pizza(serie=zip(self.labels, self.values, self.colors),
                chart_size=dp(200),
                legend_color='000000',
                legend_value_rayon=dp(70),
                legend_title_rayon=dp(125),
                chart_border=2)

        self.pizza.size_hint = (None,None)
        self.pizza.size = (dp(220), dp(220))

        pizza_padding = 50
        pizza_box = BoxLayout(size_hint=(None, None),
                            orientation='vertical')
        pizza_box.height=self.pizza.height+pizza_padding
        pizza_box.width=self.pizza.width
        pizza_box.add_widget(self.pizza)
        pizza_box.add_widget(Widget(size_hint=(None, None),
                                    size=(pizza_box.width, pizza_padding)))

        self.add_widget(pizza_box)

        self.button = CustomButton(text='Start', size_hint=(None, None), size=(dp(100), dp(50)))
        self.button.theme = ('app', 'default')
        self.add_widget(self.button)
        self.button.bind(on_release=self.button_pressed)

    def button_pressed(self, *largs):
        if self.running:
            self.running = False
            self.button.text = 'Start'
            return
        self.running = True
        self.button.text = 'Stop'
        threading.Thread(target=self.update_points).start()

    def update_points(self, *args):
        alpha = 0.95
        while self.running:
            deltas = np.random.random(6) * 30
            deltas = np.round(deltas*100)
            deltas = deltas/np.sum(deltas) * 100.0
            self.values = self.values*alpha + (1-alpha) * deltas
            self.values = np.round(self.values*100) / 100

            self.pizza.serie = zip(self.labels, self.values, self.colors)
            time.sleep(0.25)





