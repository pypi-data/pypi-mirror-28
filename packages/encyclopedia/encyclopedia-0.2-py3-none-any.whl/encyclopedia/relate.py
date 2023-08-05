# standard
from collections import OrderedDict, Mapping, MutableMapping, Iterable
import operator
import types
# internal
from encyclopedia.templates import Indexed, Unity

class Relation(Indexed):
    '''
    General purpose, discrete relation container for all mapping cardinalities:

        - 1:1 (Isomorphism)
        - 1:M (Immersion)
        - M:1 (Function e.g. Python Dictionary)
        - M:M (General Relation)

    Inversion, for all cardinalities, is provided (at the cost of doubled storage)
    '''

    CARDINALITIES = '1:1', '1:M', 'M:1', 'M:M'
    INVERTED_CARDINALITIES = {'1:1': '1:1',
                              '1:M': 'M:1', 'M:1': '1:M', 'M:M': 'M:M'}

    COMPOSITIONS = {
        '1:1': {c: c for c in CARDINALITIES},
        'M:1': {'1:1': 'M:1', 'M:1': 'M:1', '1:M': 'M:M', 'M:M': 'M:M'},
        '1:M': {'1:1': '1:M', '1:M': '1:M', 'M:1': 'M:M', 'M:M': 'M:M'},
        'M:M': {c: 'M:M' for c in CARDINALITIES}}

    unfrozen = Indexed.unfrozen

    def __init__(self,
        init=None, # can start with another dictionary, list or Relation
        cardinality='M:M', # general relation
        ordered=False, # order keys as entered
        frozen=False, # immediately make it immutable?
        ):
        '''
        Create a new Relation using a variety of different inputs
        '''
        if not ordered:
            self.forward = {}
            self.inverse = {}
        elif ordered:
            self.forward = OrderedDict()
            self.inverse = OrderedDict()
        self.ordered = ordered
        self.frozen = frozen

        if cardinality not in Relation.CARDINALITIES:
            raise Relation.Error('Invalid restriction:' + str(cardinality))
        else:
            self.cardinality = cardinality

        if init is None:
            pass
        elif isinstance(init, MutableMapping):
            self.update(init)
        elif isinstance(init, Iterable):
            for item in init:
                assert len(item) == 2
                self[item[0]] = item[1]
        else:
            assert False

    def is_ordered(self):
        return isinstance(self.forward, OrderedDict)

    def __len__(self):
        return len(self.forward)

    def values(self):
        return self.inverse.keys()

    def __iter__(self):
        return self.forward.__iter__()

    def __invert__(self):
        # NOTE: uses references .. not copies
        new = Relation(cardinality=Relation.INVERTED_CARDINALITIES[
                       self.cardinality], ordered=self.ordered)
        new.inverse = self.forward
        new.forward = self.inverse
        return new

    @staticmethod
    def _remove_from(mapping, reference):
        empty = []
        for key, values in mapping.items():
            if reference in values:
                mapping[key].remove(reference)
            if len(mapping[key]) == 0:
                empty.append(key)  # mark for removal
        for e in empty:
            del mapping[e]

    @unfrozen
    def _remove_domain(self, key):
        del self.forward[key]
        Relation._remove_from(self.inverse, key)
    __delitem__ = _remove_domain

    @unfrozen
    def _remove_range(self, key):
        del self.inverse[key]
        Relation._remove_from(self.forward, key)

    @unfrozen
    def __setitem__(self, domain, target):
        # NOTE: Relation using unconventional setitem usage: ADD instead of OVERWRITE
        if self.cardinality in ['1:1', 'M:1']:
            if domain in self.forward:
                self._remove_domain(domain)
        if self.cardinality in ['1:1', '1:M']:
            if target in self.inverse:
                self._remove_range(target)

        if self.ordered:
            self.forward.setdefault(domain, list()).append(target)
            self.inverse.setdefault(target, list()).append(domain)
        else:
            self.forward.setdefault(domain, set()).add(target)
            self.inverse.setdefault(target, set()).add(domain)

    def __getitem__(self, domain):
        if self.cardinality in ['1:1', 'M:1']:
            for target in self.forward[domain]:
                return target
        else:
            return self.forward[domain]

    @staticmethod
    def _get_cardinality(other):
        if isinstance(other, Relation):
            return other.cardinality
        elif isinstance(other, Mapping):
            return 'M:1'
        else:
            return None

    @unfrozen
    def update(self, other):
        cardinality = Relation._get_cardinality(other)
        if cardinality is None:
            raise RelationError('Cannot update:' + str(other))

        for key, value in other.items():
            if cardinality in ['1:1', 'M:1']:
                self[key] = value
            elif cardinality in ['M:M', '1:M']:
                for v in value:
                    self[key] = v
        return self

    @unfrozen
    def subtract(self, other):
        '''
        implement set difference
        '''
        cardinality = Relation._get_cardinality(other)
        if cardinality is None:
            raise RelationError('Cannot remove:' + str(other))
        for key in other:
            del self[key]
        return self

    def compose(self, other):
        '''
        Functional or relational composition
        '''
        if isinstance(other, Relation):
            new = Relation(cardinality=Relation.COMPOSITIONS[
                           self.cardinality][other.cardinality])
            for key in self:
                for middle in self.forward[key]:
                    if middle in other:
                        for value in other.forward[middle]:
                            new[key] = value
        elif isinstance(other, types.FunctionType):
            new = Relation(cardinality=self.cardinality, ordered=self.ordered)
            for key, value in self.items():
                def assign(val):
                    output = other(val)
                    if output is not None:
                        new[key] = output
                if self.cardinality in ['1:1', 'M:1']:
                    assign(value)
                else:
                    for val in value:
                        assign(val)
        elif isinstance(other, Unity):
            new=self.copy()
        else:
            assert False
        return new

    def __str__(self):
        s = []
        s.append('->')
        for d in self.forward:
            s.append(' '.join([str(d), '<', str(self.forward[d])]))
        s.append('<-')
        for ti in self.inverse:
            s.append(' '.join([str(ti), '<', str(self.inverse[ti])]))
        return '\n'.join(s)

    # cross-product operations

    def cross(self, other, op=operator.__or__):
        '''
        Experimental cross-product code ...
        '''
        def setit(x, cardinality):
            if cardinality in ['1:1', 'M:1']:
                return {x}
            elif isinstance(x, list):
                return set(x)
            else:
                return x

        new = Relation()
        for k1, v1 in self.items():
            for k2, v2 in other.items():
                for v3 in op(setit(v1, self.cardinality), setit(v2, other.cardinality)):
                    new[(k1, k2)] = v3
        return new

    class Error(Indexed.Error):
        '''
        Label Relation exceptions
        '''
        pass

# Shortcuts for Relation instantiations

class Isomorphism(Relation):

    def __init__(self, init=None, ordered=False):
        Relation.__init__(self, init, cardinality='1:1', ordered=ordered)


class Function(Relation):

    def __init__(self, init=None, ordered=False):
        Relation.__init__(self, init, cardinality='M:1', ordered=ordered)


class Partition(Relation):

    def __init__(self, init=None, ordered=False):
        Relation.__init__(self, init, cardinality='1:M', ordered=ordered)

