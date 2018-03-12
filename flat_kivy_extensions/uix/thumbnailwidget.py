
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Fbo, Translate, Color


class _ThumbNailWidget(Widget):
    ''' The :class:`ThumbNailWidget` is a widget that copies
    the canvas texture from a specified texture.
    '''

    def __init__(self, texture, **kwargs):
        #self.app = App.get_running_app()
        self.texture = texture

        super(_ThumbNailWidget, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1,1,1,1)
            self.rect_background = Rectangle(pos=self.pos, size=self.size)
        with self.canvas.after:
            self.rect = Rectangle(texture=self.texture,pos=self.pos, size=self.size)

        self.size_hint = (None, None)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
        instance.rect_background.pos = instance.pos
        instance.rect_background.size = instance.size


class ThumbNailWidget(_ThumbNailWidget):

    def __init__(self, widget, **kwargs):
        if widget.parent is not None:
            canvas_parent_index = widget.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                widget.parent.canvas.remove(self.canvas)
        fbo = Fbo(size=widget.size)
        with fbo:
            Translate(-self.x, -self.y, 0)

        fbo.add(widget.canvas)
        fbo.draw()
        super(ThumbNailWidget, self).__init__(fbo.texture)

        fbo.remove(self.canvas)

        if widget.parent is not None and canvas_parent_index > -1:
            widget.parent.canvas.insert(canvas_parent_index, widget.canvas)


