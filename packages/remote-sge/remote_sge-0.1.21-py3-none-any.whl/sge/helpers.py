# -----------------------------------------------------------
#  Copyright (C) 2009 StatPro Italia s.r.l.
#
#  StatPro Italia
#  Via G. B. Vico 4
#  I-20123 Milano
#  ITALY
#
#  phone: +39 02 96875 1
#  fax:   +39 02 96875 605
#
#  email: info@riskmap.net
#
#  This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE. See the license for more details.
# -----------------------------------------------------------
#
#  Author: Enrico Sirola <enrico.sirola@statpro.com>
#  Author: Dan Blanchard <dan.blanchard@gmail.com>

"""
internal helpers
"""

from collections import OrderedDict
from datetime import datetime

class XPathAttr(object):
    """
    Descriptor for properties on the :class:`sge.status.JobDetail` class, to
    translate values from the XML given by qstat into more readable fashion.

    See the initializer and the getter for an understanding of the mechanics.
    """
    def __init__(self, xpath, converter=None):
        """
        Args:
            xpath (str): a relative XPath query describing where to find the
                attribute.

            converter: an object with a deserialize method, which will receive
                an XML node and return the appropriate data type.
        """
        self.xpath = xpath
        self.converter = converter

    def __get__(self, instance, _):
        """
        Looks up the appropriate node on the job detail :class:`~xml.etree.ElementTree`.
        If a converter is present, calls deserialize.

        Otherwise returns the text of the found node.
        """
        xml_element = instance.xml_node.find(self.xpath)
        if self.converter:
            return self.converter.deserialize(xml_element)
        else:
            return element_text(xml_element)

class CmdOptionAttr(object):
    """
    Descriptor for properties on the JobTemplate class, to translate DRMAA options
    to properly formatted qsub options.

    A qsub option is internally identified by the option name as it is seen
    on the command line, e.g. "-V".

    Setting the attribute on a JobTemplate will result in the value being encoded
    as needed (e.g. boolean values become yes/no, etc), and then stored in the
    :func:`drmaa.JobTemplate.options` dictionary, using *option_name* as its key.

    """
    def __init__(self, option_name, type_converter=None):
        """
        Args:
            option_name (str): the name of the qsub_ option, as described
                `on the qsub man page`__.
            type_converter

        .. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
        __ qsub_
        """
        self.option_name = option_name
        self.converter = type_converter

    def __get__(self, instance, _):
        raw_value = instance.qsub_options[self.option_name]
        if self.converter:
            return self.converter.deserialize(raw_value)
        else:
            return raw_value

    def __set__(self, instance, value):
        print(instance)
        if self.converter:
            value = self.converter.serialize(value)

        instance.qsub_options[self.option_name] = value

    def __delete__(self, instance):
        print( "deleted in descriptor object")
        del instance.qsub_options[self.option_name]

def element_text(element):
    try:
        return element.text
    except AttributeError:
        pass

class XmlEnvironmentDeserializer(object):
    @staticmethod
    def deserialize(xml_node):
        res = OrderedDict()
        if xml_node != None:
            for var_el in xml_node.getchildren():
                var_name = var_el.find('VA_variable').text
                if var_name[0:14] != '__SGE_PREFIX__':
                    res[var_name] = element_text(var_el.find('VA_value'))
        return res

class XmlJobArgumentsDeserializer(object):
    @staticmethod
    def deserialize(xml_element):
        res = []
        if xml_element != None:
            for arg_el in xml_element.getchildren():
                res.append(arg_el.find('ST_name').text)
        return res

class XmlIntDeserializer(object):
    @staticmethod
    def deserialize(xml_element):
        text = element_text(xml_element)
        if text:
            return int(text)

class StringSerializer(object):
    """
    Abstract class representing how to convert between int,
    boolean or dict types, and their string representations
    that are accepted by qsub_.

    .. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
    """
    @staticmethod
    def serialize(value):
        pass
    @staticmethod
    def from_string(value):
        pass

class DictionaryConverter(StringSerializer):
    @staticmethod
    def serialize(dictionary):
        # result = []
        # for item in dictionary.items():
        #     result.append("%s=%s" % item)
        return ','.join(["%s=%s" % item for item in dictionary.items()])
    @staticmethod
    def from_string(value):
        return dict(item.split("=") for item in value.split(","))

class DateTimeConverter(StringSerializer):
    """
    Converts a python :class:`~datetime.datetime` into a string in the format
    YYYYMMDDhhmm.SS, as described in the sge datatype_ specification.

    .. _datatype: http://gridscheduler.sourceforge.net/htmlman/htmlman1/sge_types.html
    """
    FORMAT = r"%Y%m%d%H%M.%S"
    @staticmethod
    def serialize(datetime):
        return datetime.strftime(DateTimeConverter.FORMAT)
    @staticmethod
    def from_string(string):
        return datetime.strptime(string, DateTimeConverter.FORMAT)


class BoolConverter(StringSerializer):
    """Helper class to convert to/from bool attributes."""
    TRUE = r'yes'
    FALSE = r'no'

    @staticmethod
    def serialize(value):
        if value:
            return BoolConverter.TRUE
        else:
            return BoolConverter.FALSE

    @staticmethod
    def deserialize(value):
        return value == BoolConverter.TRUE


class IntConverter(StringSerializer):

    """Helper class to convert to/from int attributes."""
    @staticmethod
    def serialize(value):
        # print(value)
        return str(value)

    @staticmethod
    def deserialize(value):
        return int(value)

