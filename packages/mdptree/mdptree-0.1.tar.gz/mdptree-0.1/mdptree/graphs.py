import numpy as np
from collections import (
    ItemsView, KeysView, Mapping, MappingView, OrderedDict, Sequence, Set,
    ValuesView)
from types import GeneratorType

__all__ = ['OrientedTree']


class ImmutableDict(Mapping):
    """
    Class for immutable dict.

    """
    def __init__(self, iterable=None):
        if isinstance(iterable, GeneratorType):
            iterable = tuple(iterable)
        if iterable is None or len(iterable) == 0:
            self._keys = ()
            self._mapping = {}
            return
        if isinstance(iterable, Mapping):
            iterable = iterable.items()
        if not isinstance(self, CallableImmutableDict) and \
           all(callable(v) for k, v in iterable):
            self.__class__ = CallableImmutableDict
            self.__init__(iterable)
            return
        if not isinstance(self, IndexableImmutableDict) and \
           all(isinstance(v, (Sequence, np.ndarray)) for k, v in iterable):
            self.__class__ = IndexableImmutableDict
            self.__init__(iterable)
            return
        keys = []
        self._mapping = {}
        for k, v in iterable:
            keys.append(k)
            self._mapping[k] = v
        self._keys = tuple(keys)

    def __getitem__(self, key):
        return self._mapping[key]

    def __getattr__(self, attr):
        if '_mapping' not in self.__dict__:  # necessary when unpickling
            raise AttributeError(attr)
        return ImmutableDict((k, getattr(v, attr)) for k, v in self.items())

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def keys(self):
        return self._keys

    def items(self):
        return tuple((k, self._mapping[k]) for k in self._keys)

    def values(self):
        return tuple(self._mapping[k] for k in self._keys)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, list(self.items()))

    def __str__(self):
        return str(self._mapping)

    def _repr_pretty_(self, p, cycle):
        p.text(str(self) if not cycle else '...')


class CallableImmutableDict(ImmutableDict):
    def __call__(self, *args, **keywords):
        dispatcher = self._dispatch_args(args, keywords)
        iterable = ((key, self._mapping[key](*args_, **keywords_))
                    for key, args_, keywords_ in dispatcher)
        return ImmutableDict(iterable)

    def _dispatch_args(self, args, keywords):
        keys = set(self._keys)
        isadict = [isinstance(_, Mapping) and set(_.keys()) == keys
                   for _ in args]
        iskdict = [isinstance(_, Mapping) and set(_.keys()) == keys
                   for _ in keywords.values()]
        for key in self._keys:
            args_ = [a[key] if isadict_ else a
                     for a, isadict_ in zip(args, isadict)]
            keywords_ = {k: v[key] if iskdict_ else v
                         for (k, v), iskdict_ in zip(keywords.items(), iskdict)}
            yield key, args_, keywords_


class IndexableImmutableDict(ImmutableDict):
    def __getitem__(self, key):
        try:
            return ImmutableDict.__getitem__(self, key)
        except KeyError:
            pass
        return ImmutableDict((k, v[key]) for k, v in self.items())


class _tree_view_repr:
    def __repr__(self):
        return '{0.__class__.__name__}({1})'.format(
            self, list(self))


class tree_keys(_tree_view_repr, KeysView):
    __slots__ = ()


class tree_items(_tree_view_repr, ItemsView):
    __slots__ = ()
    def __iter__(self):
        for subtree in self._mapping._iter(self._mapping._tree):
            yield subtree[:2]
    

class tree_values(_tree_view_repr, ValuesView):
    __slots__ = ()
    def __iter__(self):
        for subtree in self._mapping._iter(self._mapping._tree):
            yield subtree[1]


class treechild_keys(_tree_view_repr, MappingView, Set):
    __slots__ = ()

    @classmethod
    def _from_iterable(self, it):
        return set(it)

    def __contains__(self, key):
        return key in iter(self)

    def __iter__(self):
        for child in self._mapping:
            yield child[0]

    def __reversed__(self):
        for child in reversed(self._mapping):
            yield child[0]


class treechild_items(_tree_view_repr, MappingView, Set):
    __slots__ = ()
    
    @classmethod
    def _from_iterable(self, it):
        return set(it)

    def __contains__(self, item):
        key, value = item
        for k, v in self:
            if k == key:
                break
        else:
            return False
        return v == value

    def __iter__(self):
        for child in self._mapping:
            yield child[:2]

    def __reversed__(self):
        for child in reversed(self._mapping):
            yield child[:2]


class treechild_values(_tree_view_repr, MappingView):
    __slots__ = ()

    def __iter__(self):
        for child in self._mapping:
            yield child[1]

    def __reversed__(self):
        for child in reversed(self._mapping):
            yield child[1]


class OrientedTree(Mapping):
    """
    Class to store one or more tree data structures as a mapping.

    The roots of the trees are considered as siblings but there is no place-
    holder for a common top-level root. Each node of each tree is identified
    by a string key.

    """
    def __init__(self):
        self._tree = []

    def __getitem__(self, key):
        for key_, val, children in self._iter(self._tree):
            if key == key_:
                return val
        raise KeyError(key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('The node key is not a string.')
        if isinstance(value, OrientedTree):
            raise NotImplementedError()
        for inode, key_, parent in self._enumerate(self._tree):
            if key == key_:
                parent[inode][1] = value
                return
        self._tree.append((key, value, []))
    
    def __delitem__(self, key):
        for ichild, child, parent in self._enumerate(self._tree):
            if child == key:
                parent.pop(ichild)
                return
        raise KeyError(key)

    def __getattr__(self, attr):
        if '_tree' not in self.__dict__:  # necessary when unpickling
            raise AttributeError(attr)
        if len(self._tree) == 0:
            raise KeyError('The tree is empty.')
        return ImmutableDict((k, getattr(v, attr)) for k, v in self.items())

    def descendants(self, key):
        """
        Return an OrientedTree instance of the descendants of a given node.

        subtree = tree.descendants(parent_key)

        Parameter
        ---------
        key : string
            The key of the parent node.

        Returns
        -------
        subtree : OrientedTree
            The OrientedTree instance which contains the trees rooted by
            each children.

        """
        for subtree in self._iter(self._tree):
            if subtree[0] == key:
                out = OrientedTree()
                out._tree = subtree[2]
                return out
        raise KeyError(key)

    @staticmethod
    def _iter(tree):
        for subtree in tree:
            yield subtree
            yield from OrientedTree._iter(subtree[2])

    @staticmethod
    def _enumerate(tree):
        for ichild, child in enumerate(tree):
            yield ichild, child[0], tree
            yield from OrientedTree._enumerate(child[2])

    @staticmethod
    def _len(tree):
        ndescendants = 0
        for subtree in tree:
            ndescendants += 1 + OrientedTree._len(subtree[2])
        return ndescendants
        
    def __iter__(self):
        for subtree in self._iter(self._tree):
            yield subtree[0]

    def keys(self):
        return tree_keys(self)

    def values(self):
        return tree_values(self)

    def items(self):
        return tree_items(self)

    def _child_list(self, key):
        if key is None:
            children = self._tree
        else:
            for key_, val, children in self._iter(self._tree):
                if key == key_:
                    break
            else:
                raise KeyError(key)
        return children

    def child_keys(self, key=None):
        return treechild_keys(self._child_list(key))

    def child_values(self, key=None):
        return treechild_values(self._child_list(key))

    def child_items(self, key=None):
        return treechild_items(self._child_list(key))

    def __len__(self):
        return self._len(self._tree)

    def _str_array(self, subtree, root):
        """
        Some box-drawing...

        """
        out = []
        for ichild, child in enumerate(subtree):
            if root:
                prefix = ''
            else:
                prefix = '└ ' if ichild == len(subtree) - 1 else '├ '
            out.append('{}{}: {!r}'.format(prefix, child[0], child[1]))
            spacer = '' if len(prefix) == 0 else '│' + (len(prefix) - 1) * ' '
            out.extend([spacer +  _ for _ in self._str_array(child[2], False)])
        return out
        
    def __str__(self):
        return '\n'.join(_ for _ in self._str_array(self._tree, True))

    def __repr__(self):
        return self.__class__.__name__ + '({!r})'.format(self._tree)

    def _repr_pretty_(self, p, cycle):
        p.text(str(self) if not cycle else '...')


if __name__ == '__main__':
    tree = OrientedTree()
    tree['a'] = 'toto'
    tree['b'] = 'titi'
    tree.descendants('b')['c'] = 'tata'
    tree.descendants('b')['d'] = 'tutu'
    tree.descendants('a')['mlkj'] = '3'
    tree.descendants('a')['000'] = 'None'
    tree.descendants('mlkj')['9'] = '348'
    tree.descendants('mlkj')['10'] = 'lkj'
    print(tree)
