# coding: utf-8
"""
Containers allow you get convenient access to different parts of document
through builtin the lxml extension, and make your code more readable.

Usage example:

    >>> class SomeStructure(Container):
    >>>     id = IntegerField('//path/to/@id')
    >>>     name = StringField('//path/to/name')
    >>>     date = DateTimeField('//path/to/@datetime', '%Y-%m-%d %H:%M:%S')

    >>> grab = Grab()
    >>> grab.go('http://exmaple.com')

    >>> structure = SomeStructure(grab)

    >>> structure.id    # 1
    >>> structure.name  # "Name of Element"
    >>> structure.date  # Return a datetime object

"""
from abc import ABCMeta, abstractmethod


class Field(object):
    """
    All custom fields should extend this class, and override the get method.
    """

    __metaclass__ = ABCMeta

    def __init__(self, xpath_exp):
        self.xpath_exp = xpath_exp

    @abstractmethod
    def get(self, container): pass


class IntegerField(Field):
    def get(self, container):
        return int(container.grab.xpath_text(self.xpath_exp))


class StringField(Field):
    def get(self, container):
        return container.grab.xpath_text(self.xpath_exp)


class DateTimeField(Field):
    def __init__(self, xpath_exp, datetime_format):
        self.datetime_format = datetime_format
        super(DateTimeField, self).__init__(xpath_exp)

    def get(self, container):
        from datetime import datetime

        datetime_str = container.grab.xpath_text(self.xpath_exp)

        return datetime.strptime(datetime_str, self.datetime_format)


class ContainerBuilder(type):
    def __new__(cls, name, base, namespace):
        _fields = {}
        for attr in namespace:
            if isinstance(namespace[attr], Field):
                field = namespace[attr]
                _fields[attr] = field
                namespace[attr] = property(field.get)

        return super(ContainerBuilder, cls).__new__(cls, name, base, namespace)


class Container(object):
    __metaclass__ = ContainerBuilder

    def __init__(self, grab):
        self.grab = grab
