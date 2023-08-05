from collections import deque
import re

from . import BaseTag
from .tags import Empty


def yield_until_nested(tag):
    if isinstance(tag, BaseTag) and not isinstance(tag, BaseNested):
        yield tag
        for child in tag.children:
            for n in yield_until_nested(child):
                yield n


def yield_only_nested(tag):
    if isinstance(tag, BaseNested):
        yield tag
    for child in tag.children:
        for n in yield_only_nested(child):
            yield n


def bracket(s, cond=True):
    return '[{}]'.format(s) if cond else ''


class BaseNested(Empty):
    is_list = False
    overwrite_property = 'name'

    def __init__(self, obj_name, *args, **kwargs):
        super(BaseNested, self).__init__(*args, **kwargs)

        self.obj_name = obj_name
        self.form_parents = deque()
        for i, child in enumerate(self.children):
            for n in yield_only_nested(child):
                if self.is_list:
                    n.form_parents.appendleft(i)
                n.form_parents.appendleft(self)

    @property
    def form_parent_strs(self):
        return [
            p.obj_name if isinstance(p, BaseNested) else str(p)
            for p in self.form_parents]

    def nested_name(self, name_attr, i):
        return 'BROTZ{}{}{}{}'.format(
            ''.join(bracket(p) for p in self.form_parent_strs),
            bracket(self.obj_name),
            bracket(i, self.is_list),
            bracket(name_attr),
        )

    @property
    def inner_str(self):
        reset_map = {}  # to reset `overwrite_property` after mutation
        for i, child in enumerate(self.children):
            for n in yield_until_nested(child):
                if self.overwrite_property in n.attributes:
                    reset_map[n] = n.attributes[self.overwrite_property]
                    n.attributes[self.overwrite_property] = self.nested_name(
                        n.attributes[self.overwrite_property], i)
        to_return = super(BaseNested, self).inner_str
        for k, v in reset_map.items():
            k.attributes[self.overwrite_property] = reset_map[k]
        return to_return


class Nested(BaseNested):
    def __repr__(self):
        return '<Nested: {}>'.format(self.obj_name)


class NestedList(BaseNested):
    is_list = True

    def __repr__(self):
        return '<NestedList: {}>'.format(self.obj_name)


class MagicList(list):
    """List that extends itself if the index to set is out of range."""
    def get(self, index):
        return None if index >= len(self) else self[index]

    def __setitem__(self, index, value):
        self += [None] * (index - len(self) + 1)
        super(MagicList, self).__setitem__(index, value)


def parse_post(post_dict):
    out = {}
    for name, value in post_dict.items():
        tmp = out
        if name.startswith('BROTZ'):
            keys = re.findall(r'\[(.+?)\]', name)
            for key, next_key in zip(keys, keys[1:] + [None]):
                if next_key is None:
                    tmp[key] = value
                    continue
                if key.isdigit():
                    key = int(key)
                if not tmp.get(key):
                    if next_key.isdigit():
                        tmp[key] = MagicList()
                    else:
                        tmp[key] = {}
                tmp = tmp[key]
    return out
