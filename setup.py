from distutils.core import setup

from sswclient import __version__
setup(name='FlatKivyExtensions', version=__version__, author='53mkramer',
      author_email='kramtek@gmail.com',
      packages=['flat_kivy_extensions',
                'flat_kivy_extensions.uix',
                'flat_kivy_extensions.third_party',
                'flat_kivy_extensions.third_party.devslib',
                ],

      data_files=[
            ('lib/python2.7/site-packages/flat_kivy_extensions',
            ['flat_kivy_extensions/ui_elements.kv',
            ]),
            ('lib/python2.7/site-packages/flat_kivy_extensions/data/font',
            [ 'flat_kivy_extensions/data/font/proximanova-bold-webfont.ttf',
             'flat_kivy_extensions/data/font/proximanova-regular-webfont.ttf',
             'flat_kivy_extensions/data/font/proximanova-semibold-webfont.ttf',
             ])],
      )

