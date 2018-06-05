
import time

from kivy.properties import (ObjectProperty, OptionProperty, NumericProperty,
                             ListProperty, StringProperty)

from kivy.animation import Animation

from kivy.uix.slider import Slider
from kivy.metrics import sp, dp
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import (StencilPush, StencilPop, StencilUse,
                           StencilUnUse, Color, Rectangle)

from flat_kivy.uix.flatslider import FlatSlider
from flat_kivy.uix.behaviors import SliderTouchRippleBehavior
from flat_kivy.uix.behaviors import GrabBehavior, ThemeBehavior

#class CustomSliderTouchRippleBehavior(SliderTouchRippleBehavior):
#    pass

class CustomSliderTouchRippleBehavior(ThemeBehavior):
    ripple_rad = NumericProperty(10)
    ripple_pos = ListProperty([0, 0])
    ripple_color = ListProperty((1., 1., 1., 1.))
    ripple_duration_in = NumericProperty(.2)
    ripple_duration_out = NumericProperty(.5)
    fade_to_alpha = NumericProperty(.75)
    ripple_scale = NumericProperty(2.0)
    ripple_func_in = StringProperty('in_cubic')
    ripple_func_out = StringProperty('out_quad')

    # slider_bar_width = NumericProperty(14)
    # slider_handle_radius = NumericProperty(16)

    slider_bar_width = NumericProperty(dp(2))
    slider_handle_radius = NumericProperty(dp(10))

    def __init__(self, **kwargs):
        super(CustomSliderTouchRippleBehavior, self).__init__(**kwargs)
        self.slider_stencil = None
        self.slider_stencil_unuse = None
        self.slider_line_stencil = None
        self.slider_line_stencil_unuse = None

    def on_touch_down(self, touch):
        if self in touch.ud:
            self.anim_complete(self, self)
            self.ripple_pos = ripple_pos = (touch.x, touch.y)
            Animation.cancel_all(self, 'ripple_rad', 'ripple_color')
            rc = self.ripple_color
            ripple_rad = self.ripple_rad
            self.ripple_color = [rc[0], rc[1], rc[2], 1.]
            anim = Animation(
                ripple_rad=max(self.width, self.height) * self.ripple_scale,
                t=self.ripple_func_in,
                ripple_color=[rc[0], rc[1], rc[2], self.fade_to_alpha],
                duration=self.ripple_duration_in)
            anim.start(self)
            with self.canvas.after:
                x,y = self.to_window(*self.pos)
                width, height = self.size

                if self.orientation == 'horizontal':
                    ellipse_pos = (self.value_pos[0] - self.slider_handle_radius, self.center_y - self.slider_handle_radius+-1*1)
                    stencil_pos = (self.x + self.padding + sp(1), self.center_y - self.slider_bar_width/2)
                    stencil_size = (self.width - self.padding * 2 - sp(0), self.slider_bar_width)
                else:
                    ellipse_pos = (self.center_x - self.slider_handle_radius+-1*1, self.value_pos[1] - self.slider_handle_radius)
                    stencil_pos = (self.center_x - self.slider_bar_width/2, self.y + self.padding + dp(1))
                    stencil_size = (self.slider_bar_width, self.height - self.padding * 2 - sp(0))

                StencilPush()
                Rectangle(
                    pos=stencil_pos,
                    size=stencil_size)
                self.slider_stencil = Ellipse(
                    pos=ellipse_pos,
                    size=(self.slider_handle_radius*2, self.slider_handle_radius*2))
                StencilUse(op='lequal')
                self.col_instruction = Color(rgba=self.ripple_color)
                self.ellipse = Ellipse(size=(ripple_rad, ripple_rad),
                    pos=(ripple_pos[0] - ripple_rad/2.,
                    ripple_pos[1] - ripple_rad/2.))
                StencilUnUse()
                Rectangle(
                    pos=stencil_pos,
                    size=stencil_size)
                self.slider_stencil_unuse = Ellipse(
                    pos=ellipse_pos,
                    size=(self.slider_handle_radius*2, self.slider_handle_radius*2))

                StencilPop()
            self.bind(ripple_color=self.set_color, ripple_pos=self.set_ellipse,
                ripple_rad=self.set_ellipse)
        return super(CustomSliderTouchRippleBehavior, self).on_touch_down(touch)

    def update_stencil(self):
        if self.orientation == 'horizontal':
            pos = [self.value_pos[0] - self.slider_handle_radius,
                   self.center_y - self.slider_handle_radius+1]
            ellipse = [self.value_pos[0] - self.slider_handle_radius,
                       self.center_y - self.slider_handle_radius+1, self.slider_handle_radius*2, self.slider_handle_radius*2]
        else:
            pos = [self.center_x - self.slider_handle_radius+1,
                   self.value_pos[1] - self.slider_handle_radius]
            ellipse = [self.center_x - self.slider_handle_radius+1,
                       self.value_pos[1] - self.slider_handle_radius, self.slider_handle_radius*2, self.slider_handle_radius*2]

        if self.slider_stencil is not None:
            self.slider_stencil.pos = pos
        if self.slider_stencil_unuse is not None:
            self.slider_stencil_unuse.pos = pos
        if self.slider_line_stencil is not None:
            self.slider_line_stencil.ellipse = ellipse
        if self.slider_line_stencil_unuse is not None:
            self.slider_line_stencil_unuse.ellipse = ellipse

    def on_value_pos(self, instance, value):
        self.update_stencil()

    def set_ellipse(self, instance, value):
        ellipse = self.ellipse
        ripple_pos = self.ripple_pos
        ripple_rad = self.ripple_rad
        ellipse.size = (ripple_rad, ripple_rad)
        ellipse.pos = (ripple_pos[0] - ripple_rad/2.,
            ripple_pos[1] - ripple_rad/2.)

    def set_color(self, instance, value):
        self.col_instruction.rgba = value

    def on_touch_up(self, touch):
        if self in touch.ud:
            rc = self.ripple_color
            anim = Animation(ripple_color=[rc[0], rc[1], rc[2], 0.],
                t=self.ripple_func_out, duration=self.ripple_duration_out)
            anim.bind(on_complete=self.anim_complete)
            anim.start(self)
        return super(CustomSliderTouchRippleBehavior, self).on_touch_up(touch)

    def anim_complete(self, anim, instance):
        self.ripple_rad = 5
        self.canvas.after.clear()
        self.slider_stencil = None
        self.slider_stencil_unuse = None



class CustomSlider(GrabBehavior, CustomSliderTouchRippleBehavior, ThemeBehavior,
                 Slider):
    color_tuple = ListProperty(['Blue', '500'])
    slider_color_tuple = ListProperty(['Orange', '300'])
    outline_color_tuple = ListProperty(['Blue', '600'])
    slider_outline_color_tuple = ListProperty(['Orange', '500'])
    ripple_color_tuple = ListProperty(['Grey', '0000'])
    released_value = NumericProperty(0.0)

    def on_touch_up(self, touch):
        now = time.time()
        if not hasattr(self, '_last_time'):
            self._last_time = 0.0
        if not hasattr(self, '_last_value'):
            self._last_value = None
            return True
        if self._last_value != self.value:
            timeDelta = now - self._last_time
            if timeDelta > 0.25:
                self._last_value = self.value
                self._last_time = now
                self.released_value = self._last_value
        return super(CustomSlider, self).on_touch_up(touch)


class ExtendedSlider(BoxLayout, ThemeBehavior):

    label_text = StringProperty('')
    label_format = StringProperty('')
    units = StringProperty('-')
    min = NumericProperty(0)
    max = NumericProperty(100)

    def __init__(self, **kwargs):
        super(ExtendedSlider, self).__init__(**kwargs)
        orientation = kwargs.get('orientation', 'horizontal')
        if orientation == 'horizontal':
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'
        self.widget = None
        self._create_widget()

    def on_theme(self, instance, value):
        self.widget.theme = value

    def _create_widget(self):
        if self.widget is not None:
            self.remove_widget(self.widget)
        if self.orientation == 'horizontal':
            self.widget = ExtendedSliderHorizontal()
        else:
            self.widget = ExtendedSliderVertical()
        self.add_widget(self.widget)

    def on_units(self, instance, value):
        if self.widget is not None:
            self.widget.units = value
            self.widget._update_label(self.widget.slider, self.widget.slider.value)

    def on_label_text(self, instance, value):
        if self.widget is not None:
            self.widget.label_text = value
            self.widget._update_label(self.widget.slider, self.widget.slider.value)

    def on_label_format(self, instance, value):
        if self.widget is not None:
            self.widget.label_format = value
            self.widget._update_label(self.widget.slider, self.widget.slider.value)

    def on_min(self, intance, value):
        if self.widget is not None:
            self.widget.min = value
            self.widget._update_label(self.widget.slider, self.widget.slider.value)

    def on_max(self, intance, value):
        if self.widget is not None:
            self.widget.max = value
            self.widget._update_label(self.widget.slider, self.widget.slider.value)


    def on_orientation(self, obj, value):
        self.orientation = value
        self._create_widget()


class _BaseExtendedSlider(BoxLayout, ThemeBehavior):

    label_text = StringProperty('')
    units = StringProperty('-')

    def _on_done_building(self):
        self.slider = self.ids.slider
        self.info_label = self.ids.label
        self.slider.bind(released_value=self._slider_released)
        self.slider.bind(value=self._update_label)
        self._update_label(self.slider, self.slider.value)

    def _slider_released(self, instance, value):
        print 'slider relased: value: %s' % str(self.slider.released_value)

    def _update_label(self, instance, value):
        a = self.label_format % value
        if isinstance(self, ExtendedSliderVertical):
            self.info_label.text = self.label_text + ':\n' + a + ' ' + self.units
        else:
            self.info_label.text = self.label_text + ': ' + a + ' ' + self.units

class ExtendedSliderHorizontal(_BaseExtendedSlider):
    pass

class ExtendedSliderVertical(_BaseExtendedSlider):
    pass


