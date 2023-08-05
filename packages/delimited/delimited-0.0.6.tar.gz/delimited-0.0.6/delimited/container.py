"""
delimited.container
~~~~~~~~~~~~~~~~~~~

This module defines NestedContainer objects. A NestedContainer object
implements an interface through which nested data can be accessed and
modified using Path objects.
"""

import abc
import copy
import collections

from delimited.path import TuplePath
from delimited.path import DelimitedStrPath


class NestedContainer(abc.ABC, dict):
    """ The abstract base class for NestedContainer objects. When subclassing
    NestedContainer the path and container attributes must be overridden with a
    Path object and container type respectively. The path object chosen defines
    the collapsed path format used by the NestedContainer class.
    """

    """ The Path object used to define paths to nested data
    """
    path = None

    """ The container type that this NestedContainer emulates
    """
    container = None

    def __init__(self, data=None):
        self(data)

    def __call__(self, data=None):
        """ Overwrite instance data with expanded data param. If data param is
        None, set instance data to new instance of container attribute.
        """

        self.data = self.container() if data is None else self._expand(data)

    def __eq__(self, other):
        """ Compare equality with instance of self or instance of container
        attribute.
        """

        if isinstance(other, self.__class__):
            return self.data == other.data
        return self.data == other

    def __ne__(self, other):
        """  Compare inequality with instance of self or instance of container
        attribute.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """ Return has of instance data.
        """

        return hash(str(self.data))

    def __bool__(self):
        """ Return instance data cast to boolean.
        """
        return bool(self.data)

    def __repr__(self):
        """ Return class name joined with instance data cast to str.
        """

        return f'{self.__class__.__name__}({self.data})'

    def __iter__(self):
        """ Yield key, value tuples for instance data.
        """

        for key, value in self.data.items():
            yield key, value

    def __contains__(self, path):
        """ Return boolean for presence of path in instance data. Accepts path
        segment or value in collapsed path format.
        """

        return self.has(path)

    def __getitem__(self, path):
        """ Return a reference to the value at path. Raise exception if path
        cannot be resolved.
        """

        return self.ref(path)

    def __setitem__(self, path, value):
        """ Set data at path to value.
        """

        self.set(path, value)

    def __delitem__(self, path):
        """ Remove key and value at path. Raise exception if path cannot be
        resolved.
        """

        self.unset(path)

    def __len__(self):
        """ Return length of first level of keys of instance data.
        """

        return len(self.data)

    def __copy__(self):
        """ Return new instance of self with its data set to a shallow copy of
        this instances data.
        """

        new = self.__class__()
        new.data = copy.copy(self.data)
        return new

    def __deepcopy__(self, *args):
        """ Return new instance of self with its data set to a deep copy of
        this instances data.
        """

        new = self.__class__()
        new.data = copy.deepcopy(self.data)
        return new

    def items(self):
        """ Yield key, value tuples for instance data.
        """

        for key, value in self.data.items():
            yield (key, value)

    def keys(self):
        """ Yield keys for instance data.
        """

        for key in self.data.keys():
            yield key

    def values(self):
        """ Yield values for instance data.
        """

        for value in self.data.values():
            yield value

    def ref(self, path=None, create=False):
        """ Return a reference to nested data at path. If create is True and
        missing key(s) are encountered while trying to resolve path, create
        the missing key(s) using an instance of self.container as the value.
        """

        # setup haystack
        haystack = self.data

        # all attributes
        if path is None:
            return haystack

        # setup path
        if not isinstance(path, self.path):
            path = self.path(path)

        # for each needle
        for needle in path:

            try:
                haystack = haystack[needle]

            except KeyError:
                if create:
                    haystack[needle] = self.container()
                    haystack = haystack[needle]

                else:
                    # TODO: custom exception
                    raise

            except TypeError:
                # TODO: custom exception
                raise

        return haystack

    def get(self, path=None, *args):
        """ Return a copy of nested data at path. First value of args is
        considered the default value, and if self.ref call raises a KeyError,
        the default value will be returned.
        """

        try:
            return copy.deepcopy(self.ref(path))
        except KeyError:
            if args:
                return args[0]
            # TODO: custom exception
            raise

        except TypeError:
            # TODO: custom exception
            raise

    def has(self, path=None):
        """ Return True if path can be resolved in instance data else False.
        """

        try:
            return bool(self.ref(path))
        except KeyError:
            return False

    def copy(self, path=None):
        """ Return a new instance of self with its data set to a deep copy of
        this instances data.
        """

        return self.__class__(self.get(path))

    def clone(self, path=None):
        """ Return a new instance of self with its data set to a reference of
        this instances data.
        """

        spawn = self.__class__()
        spawn.data = self.ref(path)
        return spawn

    @classmethod
    def _merge(cls, a, b):
        """ Recursively merge container a into a deep copy of container b
        """

        b = copy.deepcopy(b)
        for key in a.keys():

            if key in b \
                    and isinstance(a[key], cls.container) \
                    and isinstance(b[key], cls.container):
                b[key] = cls._merge(a[key], b[key])

            else:
                b[key] = a[key]

        return b

    def merge(self, data, path=None):
        """ Merge data with a copy of instance data at path and return
        merged data. Will accept instance of self or instance of
        self.container.
        """

        if isinstance(data, self.__class__):
            data = data.data
        elif isinstance(data, self.container):
            data = self.__class__(data).data
        return self._merge(data, self.get(path))

    @classmethod
    def _expand(cls, data):
        """ Recursively expand collapsed nested data and return.
        """

        expanded = cls.container()
        for path, value in data.items():

            # handle path
            if not isinstance(path, cls.path):
                path = cls.path(path)

            # expand value
            if isinstance(value, cls.container):
                value = cls._expand(value)

            for i, key in enumerate(reversed(path), 1):

                # first key
                if i == 1:
                    expanded_key = cls.container({key: value})

                # after first key
                elif i > 1:
                    expanded_key = cls.container({key: expanded_key})

                # last key, merge with other keys
                if i == len(path):
                    expanded = cls._merge(expanded, expanded_key)

        return expanded

    @classmethod
    def _collapse(cls, data, func=None, _parent_path=None):
        """ Recursively collapse expanded nested data and return.
        """

        collapsed = cls.container()
        path = _parent_path.copy() if _parent_path is not None else cls.path()

        for key, value in data.items():

            if callable(func) and func(key, value):

                if isinstance(value, cls.container) and len(value):
                    value = cls._collapse(value, func=func)

                value = cls.container({
                    path.encode(): cls.container({key: value})
                })

            else:

                path.extend(key)

                if isinstance(value, cls.container) and len(value):
                    value = cls._collapse(value, func=func, _parent_path=path)
                else:
                    value = {path.encode(): value}

            collapsed.update(value)

        return collapsed

    def collapse(self, path=None, func=None):
        """ Collapse instance data at path and return. Use func to determine
        if a level of nested data should be collapsed or not.
        """

        return self._collapse(self.get(path), func=func)

    def update(self, data, path=None):
        """ Update instance data at path with data.
        """

        haystack = self.ref(path)

        if isinstance(data, self.__class__):
            data = data.data
        elif isinstance(data, self.container):
            data = self._expand(data)

        haystack.update(data)

    def set(self, path, value, create=True):
        """ Set value at path in instance data. If create is True, create
        missing keys while trying to resolve path.
        """

        if not isinstance(path, self.path):
            path = self.path(path)

        haystack = self.ref(path.head or None, create=create)

        needle = path[-1]
        haystack[needle] = value

    def push(self, path, value, create=True):
        """ Push value to list at path in instance data. If create is True and
        key for final path segment is not set, create key and create value as
        empty list and append value to list. If create is True and key for
        final path segment is wrong type, create value as list with existing
        value and append value to list.
        """

        if not isinstance(path, self.path):
            path = self.path(path)

        haystack = self.ref(path.head, create=create)
        needle = path[-1]

        try:
            haystack[needle].append(value)

        except KeyError as e:
            if create:
                haystack[needle] = []
                haystack[needle].append(value)
            else:
                raise

        except AttributeError as e:
            if create:
                haystack[needle] = [haystack[needle]]
                haystack[needle].append(value)
            else:
                raise

        return True

    def pull(self, path, value, cleanup=False):
        """ Remove value from list at path in instance data. If cleanup is True
        and removal of value results in an empty list, remove list and key.
        """

        if not isinstance(path, self.path):
            path = self.path(path)

        haystack = self.ref(path.head or None)
        needle = path[-1]

        haystack[needle].remove(value)

        if cleanup:
            if haystack[needle] == []:
                del haystack[needle]

        return True

    def unset(self, path, cleanup=False):
        """ Remove value and last key at path. If cleanup is True and key
        removal results in empty container, recursively remove empty
        containers in reverse order of path.
        """

        if not isinstance(path, self.path):
            path = self.path(path)

        haystack = self.ref(path.head or None)
        needle = path[-1]

        del haystack[needle]

        if cleanup:
            for i, needle in enumerate(path, 1):
                if i < len(path):
                    cleanup_path = path[:(len(path) - i)]
                    if self.ref(cleanup_path) == self.container():
                        self.unset(cleanup_path)

        return True


class NestedDict(NestedContainer):
    """ This class implements tuple path notation in use with the dict
    container type.
    """

    path = TuplePath
    container = dict


class NestedOrderedDict(NestedContainer):
    """ This class implements tuple path notation in use with the OrderedDict
    container type.
    """

    path = TuplePath
    container = collections.OrderedDict


class DelimitedDict(NestedContainer):
    """ This class implements delimited string path notation in use with the
    dict container type.
    """

    path = DelimitedStrPath
    container = dict


class DelimitedOrderedDict(NestedContainer):
    """ This class implements delimited string path notation in use with the
    OrderedDict container type.
    """

    path = DelimitedStrPath
    container = collections.OrderedDict
