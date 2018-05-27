

import numpy as np

from flat_kivy_extensions.uix.customscreen import CustomScreen
from kivy.garden.pizza import Pizza

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_string('''
<-PizzaDemoScreen>:
    title: 'Pie Chart'
    theme: ('app', 'screen')
''')

class PizzaDemoScreen(CustomScreen):

    def __init__(self, *largs, **kwargs):
        super(PizzaDemoScreen, self).__init__(*largs, **kwargs)

        self.labels = ["Speech", "Noise", "Music", "Fun", "Beer"]
        self.values = np.ones(5, dtype=np.float32) * 20.0
        self.colors = ['a9a9a9', '808080', '696969', '778899', '708090']

        self.pizza = Pizza(serie=zip(self.labels, self.values, self.colors),
                chart_size=dp(200),
                legend_color='000000',
                legend_value_rayon=dp(70),
                legend_title_rayon=dp(125),
                chart_border=2)

        self.pizza.size_hint = (None,None)
        self.pizza.size = (dp(220), dp(220))

        self.add_widget(self.pizza)

        Clock.schedule_interval(self.update_points, 1 / 5.)
        self.update_points(None)


    def update_points(self, *args):
        deltas = np.random.random(5) * 30
        deltas = np.round(deltas*100)
        deltas = deltas/np.sum(deltas) * 100.0
        alpha = 0.95
        self.values = self.values*alpha + (1-alpha) * deltas
        self.values = np.round(self.values*100) / 100

        self.pizza.serie = zip(self.labels, self.values, self.colors)





