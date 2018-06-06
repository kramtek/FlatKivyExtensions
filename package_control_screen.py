
import threading, time

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget

Builder.load_string('''
<-PackageManagerScreen>:

    canvas.before:
        Color:
            rgb: 1,1,1
        Rectangle:
            pos: self.pos
            size: self.size


<CustomLabel>:
    text_size: self.size
    color: (0,0,0,1)

<ItemLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: '52dp'
    package_name: '?'
    padding: '3dp'

    canvas.before:
        Color:
            rgba: .9, .9, .9, 0.5
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: '40dp'

        CustomLabel:
            text: root.package_name
            halign: 'left'
            valign: 'middle'
            size_hint_y: None
            size_hint_x: 3.0
            height: '40dp'

        Switch:
            id: switch
            size_hint_y: None
            height: '40dp'

    BoxLayout:
        size_hint_y: None
        height: '12dp'

        CustomLabel:
            text: 'last version: '
            halign: 'left'
            size_hint_y: None
            height: '12dp'
            font_size: '10dp'

        CustomLabel:
            text: 'updated to: '
            halign: 'left'
            size_hint_y: None
            height: '12dp'
            font_size: '10dp'

            on_parent: root.done_building()
''')


class CustomLabel(Label):
    pass

class ItemLayout(BoxLayout):
    pass

    def done_building(self):
        print('done building: %s package: %s' % (str(self), str(self.package_name)))
        self.switch = self.ids.switch


def get_version(package_name):
    version = 'Not installed'
    try:
        __version__ = None
        exec('from %s import __version__' % package_name)
        version = __version__
        print 'version: %s' % str(version)
    except Exception as e:
        try:
            __ver__ = None
            exec('from %s import __ver__' % package_name)
            version = __ver__
            print 'version: %s' % str(version)
        except Exception as e:
            print '\n\nException: %s' % str(e)
    return version


class PackageVersionLayout(GridLayout):

    def __init__(self,**kwargs):
        super(PackageVersionLayout, self).__init__(**kwargs)

        label_height = 20

        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        packages = ['numpy', 'kivy', 'csv', 'flat_kivy', 'joe', 'flat_kivy_extensions']

        l = BoxLayout(size_hint_y=None, height=dp(label_height), padding=dp(10))
        label = CustomLabel(text='Package', color=(0,0,0.3,1),
                        size_hint=(None,None), size=(.45*Window.width, dp(label_height)),
                        halign='left', font_size=dp(20))
        l.add_widget(label)
        label = CustomLabel(text='Version', color=(0,0,0.3,1),
                        size_hint=(None,None), size=(.45*Window.width, dp(label_height)),
                        halign='right', font_size=dp(20))
        l.add_widget(label)
        self.add_widget(l)

        for package in packages:
            version = get_version(package)
            l = BoxLayout(size_hint_y=None, height=dp(label_height), padding=dp(10))
            label = CustomLabel(text='%s:' % package, color=(0,0,0,1),
                            size_hint=(None,None), size=(.45*Window.width, dp(label_height)),
                            halign='left')
            l.add_widget(label)
            label = CustomLabel(text='%s' % version, color=(0,0,0,1),
                            size_hint=(None,None), size=(.45*Window.width, dp(label_height)),
                            halign='right')
            l.add_widget(label)

            #switch = Switch(size_hint_y=None, height=dp(25))
            #l.add_widget(switch)

            self.add_widget(l)




class PackageInstallerLayout(GridLayout):


    def __init__(self,**kwargs):
        super(PackageInstallerLayout, self).__init__(**kwargs)
        label_height = 20

        self.spacing = dp(5)
        self.padding= dp(5)
        self.cols = 1

        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        l = BoxLayout(size_hint_y=None, height=dp(label_height), padding=dp(10))
        label = CustomLabel(text='Package', color=(0,0,0.3,1),
                        size_hint=(None,None), size=(.45*Window.width, dp(label_height)),
                        halign='left', font_size=dp(20))
        l.add_widget(label)
        label = CustomLabel(text='Install', color=(0,0,0.3,1),
                        size_hint=(None,None), size=(.45*Window.width, dp(label_height)),
                        halign='right', font_size=dp(20))
        l.add_widget(label)
        self.add_widget(l)

        self.packages = ['abc', 'def', 'hij']
        self.items = []
        for package in self.packages:
            item = ItemLayout(size_hint_y=None, height=dp(60))
            item.package_name = package
            self.add_widget(item)
            self.items.append(item)

        button = Button(text='Install Selected', size_hint_y=None, height=dp(60))
        button.bind(on_release=self.install_packages)
        self.add_widget(button)

        self.status_label = CustomLabel(text='Status: ', color=(0,0,0.3,1),
                        size_hint=(None,None), size=(.95*Window.width, dp(label_height*2)),
                        halign='left', font_size=dp(20))
        self.add_widget(self.status_label)

    def done_building(self, layout):
        print 'done building: %s' % str(layout.package_name)

    def install_packages(self, instance):
        threading.Thread(target=self._install_packages).start()

    @mainthread
    def _update_status_label(self, status):
        self.status_label.text = status

    def _install_packages(self):
        for item in self.items:
            package = item.package_name
            switch = item.switch
            if switch.active:
                self._update_status_label('Status: installing: %s' % package)
                time.sleep(2.0)
            else:
                self._update_status_label('Status: not installing: %s' % package)
                time.sleep(1.0)

        self._update_status_label('Status: ')


class PackageManagerScreen(Screen):

    def __init__(self, *largs, **kwargs):
        super(PackageManagerScreen, self).__init__(*largs, **kwargs)


        version_layout = PackageVersionLayout(cols=1, spacing=dp(5))
        installer_layout = PackageInstallerLayout(cos=1, spacing=dp(5))

        self.add_widget(version_layout)
        #self.add_widget(installer_layout)

        version_layout.add_widget(Widget(size_hint_y=None, height=dp(200)))
        #installer_layout.add_widget(Widget(size_hint_y=None, height=dp(200)))


