
from coverflow import CoverFlow, _CoreImage

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

class MyCoverFlow(CoverFlow):

    def __init__(self, covers, cover_names, *largs, **kwargs):
        self._my_covers = covers
        self._my_cover_names = cover_names
        super(MyCoverFlow, self).__init__(*largs, **kwargs)

    def get_covers(self):
        if self._my_covers is not None:
            self.lst_covers = self._my_covers
            self.cover_names = self._my_cover_names

            self.load_covers()


Builder.load_string('''
<-_OuterLayout>:
    cols: 1
    #size_hint_y: None
    #height: dp(500)
    canvas.before:
        Color:
            rgba: (0.1, 0.5, 0.95, 0.5)
        Rectangle:
            size: self.size
            pos: self.pos
''')


class _OuterLayout(GridLayout):
    pass

class CoverFlowLayout(_OuterLayout):
    def __init__(self, covers, cover_names, cover_change_callback=None, **kwargs):
        super(CoverFlowLayout, self).__init__(**kwargs)

        self.cover_change_callback = cover_change_callback

        #self.coverflow = MyCoverFlow(ncovers=4, path='/Users/kramer/mobilabui/data/images', pos3D=(0,4,-2), cover_rotation=45)
        self.coverflow = MyCoverFlow(covers, cover_names, ncovers=3, pos3D=(0,4,-2), cover_rotation=45, move_duration=0.25)
        #self.coverflow = MyCoverFlow(ncovers=4, pos3D=(0,4,-2), cover_rotation=45)
        self.coverflow.cover_separation = 75
        self.coverflow.scale_x = 0.57/dp(1)
        self.coverflow.scale_y = 0.57/dp(1)

        #self.coverflow.size_hint_y = None
        #self.coverflow.height = dp(400)
        self.add_widget(self.coverflow)

        self.moved = False

#        self.coverflow.size_hint_y = None
#        self.coverflow.height = dp(400)

#        print 'cf size: %s'  % str(self.coverflow.size)
#        print 'cf size hint: %s'  % str(self.coverflow.size_hint)

        if False:
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)


#    def do_layout(self, *largs):
#        print 'do layout...'
#        super(CoverFlowLayout, self).do_layout(*largs)

#    def on_size(self, *largs):
#        print 'on size...'

    def on_touch_move(self, touch):
#        print 'cf size: %s'  % str(self.coverflow.size)
#        print 'cf size hint: %s'  % str(self.coverflow.size_hint)
#        print 'Window size: %s'  % str(Window.size)
#        for cover in self.coverflow.covers:
#            print 'cover: %s'  %str(cover.scale_y)


#        print 'current index: %s' % str(self.coverflow.current_index)
        swipe_threshold = dp(50)
        if (touch.x - touch.ox) > swipe_threshold:
            self.moved = True
            self.coverflow.move_to_right()
        if (touch.ox - touch.x) > swipe_threshold:
            self.moved = True
            self.coverflow.move_to_left()

    def on_touch_up(self, touch):
        if self.moved:
            self.moved = False
            return
        if abs(touch.x - Window.width/2.0) < dp(50):
            ind = self.coverflow.current_index
#            print 'should navigate to index: %s' % str(ind)
            if self.cover_change_callback is not None:
                self.cover_change_callback(self.coverflow.current_index)

        if (touch.x - Window.width/2.0) > dp(100):
            self.coverflow.move_to_left()
        if -(touch.x - Window.width/2.0) > dp(100):
            self.coverflow.move_to_right()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'escape':
            keyboard.release()

        if keycode[1] == 'left':
            self.coverflow.move_to_left()

        if keycode[1] == 'right':
            self.coverflow.move_to_right()

#        print 'current index: %s' % str(self.coverflow.current_index)


if __name__ == '__main__':
    from kivy.base import runTouchApp

    lst_covers = [
      '/Users/kramer/mobilabui/data/images/python.png',
      '/Users/kramer/mobilabui/data/images/icube_0.png',
      '/Users/kramer/mobilabui/data/images/copain_0.png',
      '/Users/kramer/mobilabui/data/images/hi_left_blue.png',
      '/Users/kramer/mobilabui/data/images/python.png',
      '/Users/kramer/mobilabui/data/images/hi_left_blue.png',
      '/Users/kramer/mobilabui/data/images/python.png',
      '/Users/kramer/mobilabui/data/images/hi_left_blue.png',
      '/Users/kramer/mobilabui/data/images/python.png',
    ]
    covers = list()

    cover_names = list()
    for name in lst_covers:
        covers.append(_CoreImage(name))
        cover_names.append(name)

    runTouchApp(CoverFlowLayout(covers, cover_names, None) )

