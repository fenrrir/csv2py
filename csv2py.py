# Copyright 2017 Rodrigo Pinheiro Marques de Araujo <fenrrir@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc
import codecs
import six


class DataFormat(Exception):
    pass


@six.add_metaclass(abc.ABCMeta)
class Loader(object):

    def before_loader(self):
        pass

    def after_loader(self):
        pass

    @abc.abstractmethod
    def run(self):
        raise TypeError()


class CSVLoader(Loader):
    line_loaders = []
    reader_class = None

    def __init__(self, file, encoding, delimiter, initial_context=None):
        self.file = file
        self.encoding = encoding
        self.delimiter = delimiter
        self.initial_context = initial_context or dict()

    def run(self):
        self.before_loader()
        with codecs.open(self.file, encoding=self.encoding) as f:
            reader = self.reader_class(f, delimiter=self.delimiter)
            for line in reader:
                context = dict(self.initial_context)
                self.before_line_loader(line)
                for cls_loader in self.line_loaders:
                    loader = cls_loader(line, context=context)
                    loader.run()
                self.after_line_loader(line, context=context)
        self.after_loader()

    def before_line_loader(self, line):
        pass

    def after_line_loader(self, line, context):
        pass


class Field(object):

    def __init__(self, target_attribute, index=None, source_attribute=None, required=True, validators=None, type=str):
        if not (index or source_attribute):
            raise ValueError('index or source_name must be defined')
        if index and source_attribute:
            raise ValueError('index and source_name defined')

        self.item = index if index else source_attribute
        self.target_attribute = target_attribute
        self.required = required
        self.type = type
        self.validators = validators if validators else []

    def get_value(self, loader, line):
        try:
            value = line[self.item]
        except (IndexError, KeyError) as error:
            if self.required:
                raise DataFormat('field is missing')
            else:
                value = ''

        value = self.clean(loader, value)

        return self.type(value)

    def clean(self, loader, value):

        for validator in self.validators:
            validator(value)

        loader_clean_name = 'clean_' + self.target_attribute
        if hasattr(loader, loader_clean_name):
            loader_clean = getattr(loader, loader_clean_name)
            value = loader_clean(value)

        return value


@six.add_metaclass(abc.ABCMeta)
class BaseCSVLineLoader(object):
    context_name = None
    fields = []
    unique_attrs = []
    context_requires = []

    def __init__(self, line, context):
        self.line = line
        self.context = context

    def run(self):
        data = self.get_data()
        if self.unique_attrs:
            key = self.get_object_key(data)
            obj = self.get_object(key)
            if obj:
                self.update_object(obj, data)
                self.update_context(obj)
                return

        obj = self.create_object(data)
        self.update_context(obj)

    def update_context(self, obj):
        self.context[self.context_name] = obj

    @abc.abstractmethod
    def get_object(self, key):
        pass

    @abc.abstractmethod
    def create_object(self, data):
        pass

    @abc.abstractmethod
    def update_object(self, obj, data):
        pass

    def get_object_key(self, data):
        key = {}
        for attr in self.unique_attrs:
            key[attr] = data[attr]
        return key

    def get_initial_data(self):
        data = {}
        for name in self.context_requires:
            data[name] = self.context[name]
        return data

    def get_data(self):
        data = self.get_initial_data()
        for field in self.fields:
            data[field.target_attribute] = field.get_value(self, self.line)
        return data


class DjangoCSVLineLoader(BaseCSVLineLoader):
    model = None

    def get_object(self, key):
        try:
            return self.model.objects.get(**key)
        except self.model.DoesNotExist:
            return

    def create_object(self, attrs):
        return self.model.objects.get_or_create(**attrs)[0]

    def update_object(self, obj, attrs):
        self.model.objects.filter(id=obj.id).update(**attrs)
