
header = {
    'CustomIconButton': {
        'color_tuple': ('Brown', '900'),
        'font_color_tuple': ('Gray', '100'),
        'style': 'Button',
        'icon_color_tuple': ('Gray', '100'),
        'icon_font_size' : '25dp',
    },
    'FlatLabel': {
        'color_tuple' : ('Orange', '500'),
        'style' : 'HeaderTitle',
    },
}

tabbarbutton = {
    'FlatIconButton': {
     },
    'CustomIconButton': {
        'color_tuple': ('Brown', '50'),
        'font_color_tuple': ('Brown', '900'),
        'icon_color_tuple': ('BlueGray', '800'),
        'content_padding' : ['3dp', '2dp', '2dp', '0dp'],
        'style': 'NavigationButton',
        'font_size' : '11dp',
        'icon_font_size' : '12dp',
        'orientation' : 'tb-rl',
    },
}
tabbarbutton_highlighted = {
    'FlatIconButton': {
     },
    'CustomIconButton': {
        'color_tuple': ('BlueGray', '800'),
        'font_color_tuple': ('Brown', '50'),
        'icon_color_tuple': ('BlueGray', '200'),
        'content_padding' : ['3dp', '2dp', '2dp', '0dp'],
        'style': 'NavigationButton',
        'font_size' : '11dp',
        'icon_font_size' : '18dp',
        'orientation' : 'tb-rl',
    },
}

navigationdrawer = {
    'FlatLabel': {
        'size_hint_y' : None,
        'height' : '15dp',
        # 'font_size' : '20dp',
        'color_tuple' : ('Green', '300'),
        'style' : 'NavigationLabelMainHeading',
    },
    'FlatIconButton': {
        #'color_tuple': ('Brown', '800'),
        #'font_color_tuple': ('Blue', '300'),
        #'size_hint_y' : None,
        #'height' : '35dp',
        #'icon' : 'fa-chevron-right',
        #'icon_color_tuple': ('Red', '500'),
        #'padding' : '3dp',
        #'style': 'NavigationButton',
    },
    'CustomIconButton': {
        'color_tuple': ('Brown', '800'),
        'font_color_tuple': ('Blue', '300'),
        'size_hint_y' : None,
        'height' : '40dp',
        'icon' : 'fa-chevron-right',
        'icon_color_tuple': ('Red', '500'),
        'icon_font_size' : '15dp',
        'content_padding' : ['3dp', '2dp', '2dp', '0dp'],
        'style': 'NavigationButton',
        'orientation' : 'rl-tb',
    },
}

screen = {
    'FlatLabel': {
        'color_tuple' : ('Brown', '800'),
        'style' : 'HeaderTitle',
        'size_hint_y' : None,
        'height' : '40dp',
    },
}

grouped_layout = {
    'FlatLabel': {
        'color_tuple': ('Brown', '800'),
        'style': 'GroupedLayoutTitle',
        'size_hint_y': None,
        'height': '25dp',
    },
}

popup = {
    'CustomButton': {
        'color_tuple': ('Brown', '500'),
        'font_color_tuple': ('Gray', '100'),
        'style': 'CustomButton1',
        'radius' : '2dp',
    },
    'CustomBusyContent': {
        'color_tuple': ('Brown', '500'),
        'font_color_tuple': ('Gray', '400'),
        'style': 'CustomButton1',
        'radius' : '2dp',
    },
}

default = {
    'CustomButton': {
        'color_tuple': ('Brown', '500'),
        'font_color_tuple': ('Gray', '100'),
        'style': 'CustomButton1',
        'radius' : '10dp',
    },
    'CustomCheckBoxListItem': {
        'font_color_tuple': ('Blue', '800'),
        'check_color_tuple': ('Green', '600'),
        'check_color_hue_down': '200',
        'outline_color_tuple': ('Gray', '500'),
        'style': 'Button',
        'valign' : 'middle',

        'size_scaling' : 0.5,
        'outline_size': '1.5dp',
        'style': 'CustomButton1',

        'check_scale': .5,
        'radius' : '4dp',
        'icon' : 'fa-check',
    },
    'CustomSwitchListItem': {
        'style': 'LabelNormalBold',
        'valign' : 'bottom',
        'switch_font_size' : '2dp',
        'height' : '30dp',
        'scaling' : 1.0,
    },

    'FlatCheckBoxListItem': {
    },

    'ExtendedSliderHorizontal': {
        #'color_tuple': ('Green', '600'),
        #'outline_color_tuple': ('Blue', '500'),
        #'slider_color_tuple': ('Red', '100'),
        #'slider_outline_color_tuple': ('Yellow', '700'),
        #'ripple_color_tuple': ('Orange', '200'),
        #'slider_bar_width' : '0.1dp',
        #'outline_width' : '0.5dp',
        'font_color_tuple' : ('Purple', '800'),
    },
    'ExtendedSliderVertical': {
        #'color_tuple': ('Brown', '600'),
        #'outline_color_tuple': ('Green', '900'),
        #'slider_color_tuple': ('Blue', '200'),
        #'slider_outline_color_tuple': ('Gray', '700'),
        #'ripple_color_tuple': ('Pink', '200'),
        #'slider_bar_width' : '0.1dp',
        #'outline_width' : '0.5dp',
        'font_color_tuple' : ('Blue', '500'),
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
    'app' : {'header' : header,
             'navigationdrawer' : navigationdrawer,
             'tabbarbutton' : tabbarbutton,
             'tabbarbutton_highlighted' : tabbarbutton_highlighted,
             'screen' : screen,
             'grouped_layout' : grouped_layout,
             'default' : default,
             'shit' : popup,
             }
}

from flat_kivy_extensions.uix.custombutton import CustomButton
from flat_kivy_extensions.uix.customiconbutton import CustomIconButton
from flat_kivy_extensions.uix.customslider import CustomSlider, CustomSliderTouchRippleBehavior, ExtendedSlider, ExtendedSliderVertical, ExtendedSliderHorizontal
from flat_kivy_extensions.uix.customcheckbox import CustomCheckBoxListItem, CustomSwitchListItem
from flat_kivy_extensions.uix import CustomBusyContent

types_to_theme = {
    'CustomSlider' : CustomSlider,
    'ExtendedSlider' : ExtendedSlider,
    'ExtendedSliderHorizontal' : ExtendedSliderHorizontal,
    'ExtendedSliderVertical' : ExtendedSliderVertical,
    'CustomSliderTouchRippleBehavior': CustomSliderTouchRippleBehavior,
    'CustomButton' : CustomButton,
    'CustomIconButton' : CustomIconButton,
    'CustomCheckBoxListItem' : CustomCheckBoxListItem,
    'CustomSwitchListItem' : CustomSwitchListItem,
    'CustomBusyContent' : CustomBusyContent,
    # 'FlatIconButtonLeft' : FlatIconButtonLeft,
}

from utils import relative_path_to_fonts

font_styles = {
    'HeaderTitle': {
        'font': '%s/proximanova-semibold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (18, 'sp'), 'desktop': (18, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'NavigationButton': {
        'font': '%s/proximanova-regular-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (14, 'sp'), 'desktop': (14, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'NavigationLabelMainHeading': {
        'font': '%s/proximanova-bold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (14, 'sp'), 'desktop': (14, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'NavigationLabelSubHeading': {
        'font': '%s/proximanova-bold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (15, 'sp'), 'desktop': (15, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'GroupedLayoutTitle': {
        'font': '%s/proximanova-bold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (17, 'sp'), 'desktop': (17, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'CustomButton1': {
        'font': '%s/proximanova-semibold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (15, 'sp'), 'desktop': (15, 'sp')},
        'alpha': .87,
        'wrap': False,
    },

    'LabelNormal': {
        'font': '%s/proximanova-regular-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (15, 'sp'), 'desktop': (15, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'LabelNormalBold': {
        'font': '%s/proximanova-semibold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (15, 'sp'), 'desktop': (15, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'LabelSmall': {
        'font': '%s/proximanova-regular-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (12, 'sp'), 'desktop': (12, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'LabelSmallBold': {
        'font': '%s/proximanova-semibold-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (12, 'sp'), 'desktop': (12, 'sp')},
        'alpha': .87,
        'wrap': False,
    },
    'LabelTiny': {
        'font': '%s/proximanova-regular-webfont.ttf' % relative_path_to_fonts,
        'sizings': {'mobile': (10, 'sp'), 'desktop': (10, 'sp')},
        'alpha': .87,
        'wrap': False,
    },


}
