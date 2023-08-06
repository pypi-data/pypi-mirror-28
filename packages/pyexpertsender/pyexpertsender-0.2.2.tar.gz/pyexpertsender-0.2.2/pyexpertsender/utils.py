import xml.etree.ElementTree as ET

xsi = 'http://www.w3.org/2001/XMLSchema-instance'
xs = 'http://www.w3.org/2001/XMLSchema'


def camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate_entity(data, parent):
    if isinstance(data, dict):
        for key, data in data.iteritems():
            if key == 'text':
                parent.text = unicode(data)
            elif key == 'attrs':
                for attr, val in data.iteritems():
                    parent.set('xsi:' + attr, val)
            else:
                child = ET.SubElement(parent, camel_case(key))
                generate_entity(data, child)
    elif isinstance(data, list):
        for value in data:
            generate_entity(value, parent)
    else:
        parent.text = unicode(data)


def generate_request_xml(api_key, data_type, dict_tree):
    root = ET.Element('ApiRequest')
    root.set('xmlns:xsi', xsi)
    root.set('xmlns:xs', xs)
    api_key_element = ET.SubElement(root, 'ApiKey')
    api_key_element.text = api_key
    if data_type:
        dict_tree['attrs'] = {'type': data_type}
    generate_entity({'data': dict_tree}, root)

    return ET.tostring(root)
