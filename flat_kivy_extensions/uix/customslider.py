
from kivy.properties import (ObjectProperty, OptionProperty, NumericProperty,
                             ListProperty, StringProperty)

from kivy.animation import Animation

from kivy.uix.slider import Slider
from kivy.metrics import sp, dp
from kivy.animation import Animation
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

    slider_bar_width = NumericProperty(14)
    slider_handle_radius = NumericProperty(16)

    slider_bar_width = NumericProperty(3)
    slider_handle_radius = NumericProperty(12)

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
                    ellipse_pos = (self.value_pos[0] - sp(self.slider_handle_radius), self.center_y - sp(self.slider_handle_radius+1))
                    stencil_pos = (self.x + self.padding + sp(1), self.center_y - sp(self.slider_bar_width/2))
                    #stencil_size = (self.width - self.padding * 2 - sp(2), self.slider_bar_width)
                    stencil_size = (self.width - self.padding * 2 - sp(2), 4)
                else:
                    ellipse_pos = (self.center_x - sp(self.slider_handle_radius+1), self.value_pos[1] - sp(self.slider_handle_radius))
                    stencil_pos = (self.center_x - sp(self.slider_bar_width/2), self.y + self.padding + sp(1))
                    stencil_size = (sp(self.slider_bar_width), self.height - self.padding * 2 - sp(2))

                StencilPush()
                Rectangle(
                    pos=stencil_pos,
                    size=stencil_size)
                self.slider_stencil = Ellipse(
                    pos=ellipse_pos,
                    size=(sp(self.slider_handle_radius*2), sp(self.slider_handle_radius*2)))
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
                    size=(sp(self.slider_handle_radius*2), sp(self.slider_handle_radius*2)))

                StencilPop()
            self.bind(ripple_color=self.set_color, ripple_pos=self.set_ellipse,
                ripple_rad=self.set_ellipse)
        return super(CustomSliderTouchRippleBehavior, self).on_touch_down(touch)

    def update_stencil(self):
        if self.orientation == 'horizontal':
            pos = [self.value_pos[0] - sp(self.slider_handle_radius),
                   self.center_y - sp(self.slider_handle_radius+1)]
            ellipse = [self.value_pos[0] - sp(self.slider_handle_radius),
                       self.center_y - sp(self.slider_handle_radius+1), sp(self.slider_handle_radius*2), sp(self.slider_handle_radius*2)]
        else:
            pos = [self.center_x - sp(self.slider_handle_radius+1),
                   self.value_pos[1] - sp(self.slider_handle_radius)]
            ellipse = [self.center_x - sp(self.slider_handle_radius+1),
                       self.value_pos[1] - sp(self.slider_handle_radius), sp(self.slider_handle_radius*2), sp(self.slider_handle_radius*2)]

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

    # slider_bar_width = NumericProperty(16)
    # slider_handle_radius = NumericProperty(16)
    #
    # slider_bar_width = NumericProperty(3)
    # slider_handle_radius = NumericProperty(12)
    pass


