from urllib import parse as urllib_parse
from xml.etree import ElementTree

import requests
from flask import current_app, request


def cas_verify_ticket(ticket):
    protocol = 'https' if request.is_secure else 'http'
    service_url = urllib_parse.urlunparse(
        (protocol, request.host, request.path, '', '', '')
    )

    params = {
        'ticket': ticket,
        'service': service_url,
    }
    response = requests.get(current_app.config.get('CAS_VALIDATE_URL'), params=params)
    current_app.logger.debug('response.ok: %s', response.ok)
    if response.ok:
        username = None
        # attributes = {}
        # pgtiou = None

        tree = ElementTree.fromstring(response.text)
        if tree[0].tag.endswith('authenticationSuccess'):
            """ Get namespace for looking for elements by tagname """
            namespace = tree.tag[0:tree.tag.index('}') + 1]
            username = tree[0].find('.//' + namespace + 'user').text
            # for element in tree[0]:
            #     if element.tag.endswith('proxyGrantingTicket'):
            #         pgtiou = element.text
            #     elif element.tag.endswith('attributes') or element.tag.endswith('norEduPerson'):
            #         attributes = parse_attributes_xml_element(element)
        current_app.logger.debug('username: %s', username)
        return username
    return None


def parse_attributes_xml_element(element):
    attributes = {}
    for attribute in element:
        tag = attribute.tag.split("}").pop()
        if tag in attributes:
            if isinstance(attributes[tag], list):
                attributes[tag].append(attribute.text)
            else:
                attributes[tag] = [attributes[tag]]
                attributes[tag].append(attribute.text)
        else:
            if tag == 'attraStyle':
                pass
            else:
                attributes[tag] = attribute.text
    return attributes
