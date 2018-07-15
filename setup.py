from distutils.core import setup

from flat_kivy_extensions import __version__

spPath = 'lib/python2.7'
import platform
if platform.system().startswith('Windows'):
    spPath = 'Lib'


setup(name='FlatKivyExtensions', version=__version__, author='53mkramer',
      author_email='kramtek@gmail.com',
      packages=['flat_kivy_extensions',
                'flat_kivy_extensions.uix',
                'flat_kivy_extensions.third_party',
                'flat_kivy_extensions.third_party.devslib',
                ],

      data_files=[
            ('%s/site-packages/flat_kivy_extensions' % spPath,
            ['flat_kivy_extensions/ui_elements.kv',
            ]),
            ('%s/site-packages/flat_kivy_extensions/data/font' % spPath,
            [ 'flat_kivy_extensions/data/font/proximanova-bold-webfont.ttf',
             'flat_kivy_extensions/data/font/proximanova-regular-webfont.ttf',
             'flat_kivy_extensions/data/font/proximanova-semibold-webfont.ttf',
             ])],
      )

