import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_relative_font_path(local_font_path):
    ''' Get the relative path from the font path specified to the flat_kivy font
    paths so they can be added by flat_kivy
    '''
    import flat_kivy
    flat_kivy_font_path = os.path.join(os.path.dirname(os.path.abspath(flat_kivy.__file__)), *['data', 'font'])

    paths = [flat_kivy_font_path, local_font_path]
    common_prefix = os.path.commonprefix(paths)
    relative_paths = [os.path.relpath(path, common_prefix) for path in paths]
    # components = relative_paths[0].split(os.sep)
    relative_path_to_extensions = os.sep.join(['..'] * len(relative_paths[0].split(os.sep)))
    relative_path_to_fonts = os.path.join(relative_path_to_extensions, relative_paths[1])
    return relative_path_to_fonts

import flat_kivy_extensions
local_font_path = os.path.join(os.path.dirname(os.path.abspath(flat_kivy_extensions.__file__)),
                                        *['data', 'font'])
relative_path_to_fonts = get_relative_font_path(local_font_path)

from . import PackageLogger
log = PackageLogger(__name__, moduleDebug=True)

def is_app_config_available():
    filename = 'local_app_config.xml'
    try:
        tree = ET.ElementTree(file=filename)
        current_root = tree.getroot()
    except Exception as e:
        log.error('Exception: %s  (returning None)' % str(e))
        return False
    return True

localTree = None
def get_app_config_entry(configTag, forceReload=True):
    global localTree
    if forceReload or localTree is None:
        filename = 'local_app_config.xml'
        try:
            print('loading tree fresh from %s'  % filename)
            tree = ET.ElementTree(file=filename)
            localTree = tree
        except Exception as e:
            log.error('Exception: %s  (returning None)' % str(e))
            return None
    else:
        print('using pre-loaded tree...')
    current_root = localTree.getroot()
    return current_root.find(configTag)


def prettify(elem):
    roughString = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(roughString)
    return reparsed.toprettyxml(indent="  ")

def set_app_config_entry(configTags, tags, attributes):
    filename = 'local_app_config.xml'
    global localTree
    try:
        if localTree is None:
            tree = ET.ElementTree(file=filename)
        else:
            tree = localTree
        current_root = tree.getroot()
    except Exception as e:
        log.error('Exception: %s  (returning None)' % str(e))
        return None

    element = current_root
    for tag in configTags:
        parent = element
        element = element.find(tag)

    parent.remove(element)
    element = ET.SubElement(parent, tag)

    for (tag, attrib) in zip(tags, attributes):
        el = ET.SubElement(element, tag)
        el.attrib = attrib

    with open(filename, 'w+') as outputFile:
        outputFile.write(prettify(current_root))




