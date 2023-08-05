# Copyright 2017-2018 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import collections

import yaml
from yaml.dumper import Dumper


class Node(collections.MutableMapping):
    """
    This class is a base class to add typesafe objects to a Config.
    Example:

    >>> from dewi.config.config import Config
    >>> class A(Node):
    >>>     entry: str = 'default-value'
    >>> c = Config()
    >>> c.set('root', A())
    """

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __setattr(self, key, value):
        if key not in self:
            raise KeyError(key)
        super().__setattr__(key, value)

    def __iter__(self):
        return iter(self.__dict__)

    def __delitem__(self, key):
        raise RuntimeError('Unable to delete key {}'.format(key))

    def __repr__(self):
        return str(self.__dict__)

    def load_from(self, data: dict):
        load_node(self, data)


def load_node(node: Node, d: dict):
    for key, value in d.items():
        if key in node and isinstance(node[key], Node):
            node[key].load_from(value)
        else:
            node[key] = value

def represent_node(dumper: Dumper, data: Node):
    return dumper.represent_dict(data)


yaml.add_multi_representer(Node, represent_node)
