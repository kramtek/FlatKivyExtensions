main = {
    'FlatButton': {
        'color_tuple': ('Gray', '0000'),
        'font_color_tuple': ('LightGreen', '800'),
        'style': 'Button',
    },
    'RaisedFlatButton': {
        'color_tuple': ('Gray', '0000'),
        'font_color_tuple': ('LightGreen', '800'),
        'style': 'Button',
    },
    'FlatLabel': {
        'style': 'Button',
    },
    'FlatSlider': {
        'bar_fill_color_tuple': ('LightGreen', '500'),
        'handle_accent_color_tuple': ('LightGreen', '200'),
    },
}

accent = {
    'FlatButton': {
        'color_tuple': ('LightGreen', '500'),
        'font_color_tuple': ('Gray', '1000'),
        'style': 'Button',
    },
    'RaisedFlatButton': {
        'color_tuple': ('LightGreen', '500'),
        'font_color_tuple': ('Gray', '1000'),
        'style': 'Button',
    },
    'FlatIconButton': {
        'color_tuple': ('LightGreen', '500'),
        'font_color_tuple': ('Gray', '1000'),
        'style': 'Button',
        'icon_color_tuple': ('Gray', '1000')
    },
    'FlatToggleButton': {
        'color_tuple': ('LightGreen', '500'),
        'font_color_tuple': ('Gray', '1000'),
        'style': 'Button',
    },
    'RaisedFlatToggleButton': {
        'color_tuple': ('LightGreen', '500'),
        'font_color_tuple': ('Gray', '1000'),
        'style': 'Button',
    },
    'FlatCheckBox': {
        'color_tuple': ('Gray', '0000'),
        'check_color_tuple': ('LightGreen', '500'),
        'outline_color_tuple': ('Gray', '1000'),
        'style': 'Button',
        'check_scale': .7,
        'outline_size': '10dp',
    },
    'FlatCheckBoxListItem': {
        'font_color_tuple': ('Gray', '1000'),
        'check_color_tuple': ('LightGreen', '500'),
        'outline_color_tuple': ('Gray', '800'),
        'style': 'Button',
        'check_scale': .7,
        'outline_size': '10dp',
    },
}


navigationdrawer = {
    'FlatLabel': {
        'size_hint_y' : None,
        'height' : '15dp',
        # 'font_size' : '20dp',
        'color_tuple' : ('Gray', '1000'),
        'style' : 'NavigationLabelMainHeading',
    },

    'CustomIconButton': {
        #'color_tuple': ('Gray', '1000'),
        'color': [.9, .9, .8, 1.0],
        'font_color_tuple': ('Gray', '1000'),
        'size_hint_y' : None,
        'height' : '40dp',
        'icon' : 'fa-chevron-right',
        'icon_color_tuple': ('Gray', '1000'),
        'icon_font_size' : '15dp',
        'content_padding' : ['3dp', '2dp', '2dp', '0dp'],
        'style': 'NavigationButton',
        'orientation' : 'tb-lr',
    },
}

header = {
    'CustomIconButton': {
        'font_color_tuple': ('Gray', '100'),
        'style': 'Button',
        'icon_color_tuple': ('Gray', '200'),
        'icon_font_size' : '25dp',
    },
    'FlatLabel': {
        'color_tuple' : ('Gray', '200'),
        'style' : 'HeaderTitle',
    },
}

default = {
    'CustomButton': {
        'color_tuple': ('Brown', '800'),
        'font_color_tuple': ('Gray', '100'),
        'style': 'CustomButton1',
        'radius' : '5dp',
    },
    'CustomCheckBoxListItem': {
        'font_color_tuple': ('Blue', '800'),
        'check_color_tuple': ('Green', '600'),
        'check_color_hue_down': '200',
        'outline_color_tuple': ('Gray', '500'),
        'style': 'LabelNormalBold',
        'valign' : 'middle',

        'size_scaling' : 0.5,
        'outline_size': '1.5dp',

        'check_scale': .5,
        'radius' : '4dp',
        'icon' : 'fa-check',
    },
    'CustomSwitchListItem': {
        'style': 'LabelNormalBold',
        'valign' : 'middle',
        # 'font_size' : '20dp',
        'switch_font_size' : '6dp',
    },
    'CustomSliderTouchRippleBehavior': {
        'slider_bar_width' : '2dp',
        'slider_handle_radius' : '10dp',
    },
    'CustomSlider': {
        'color_tuple': ('Brown', '600'),
        'outline_color_tuple': ('Green', '900'),
        'slider_color_tuple': ('Brown', '100'),
        'slider_outline_color_tuple': ('Brown', '700'),
        'ripple_color_tuple': ('Brown', '200'),
        'slider_bar_width' : '0.1dp',
        'outline_width' : '0.5dp',
    },
}

themes = {
    'green': {'main': main,
              'accent': accent,
              },
    'app' : {'navigationdrawer' : navigationdrawer,
             'header' : header,
             'default' : default,
             },
}

