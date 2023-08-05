# standard
import unittest
import hashlib
import types
# internal
from encyclopedia.templates import Unindexed
from encyclopedia.relate import Relation

class Forest(Unindexed):
    '''
    An Encyclopedia of trees

    Note: there is no specific "Tree" class; instead, a Tree is Forest with 1 connected (tree) graph.
    This is purposeful: adding two Trees creates a Forest, not another Tree.

    Terminology of this class:

    - Tree: single, connected (tree) graph
    - Forest: a (possibly empty) collection of Trees, supporting Unindexed Encyclopedia operations
    - Node: a single node in a graph (as usual)
    - Twig: a connected pair of nodes
    - Sprout: a new, connected node

    '''
    def __init__(self,
        offset:int = 0, # starting node counter
        parent = None):# for future use ...
        '''
        Create the forest
        '''
        self.trees = set() # *disconnected* set of tree graphs
        self.aliases = Relation(cardinality='1:M') # alias -> node(s)
        self.nodes = Relation(cardinality='1:M') # node -> upper node(s)
        self.levels = Relation(cardinality='M:1') # node(s) -> level
        self.counter = offset # counter used for creating unique Node IDs
        self.parent = parent # future use for referencing originating forest (where applicable)
        self.frozen = False # start off mutable

    unfrozen = Unindexed.unfrozen

    def __iter__(self):
        '''
        Notes: creates Forest.keys() via mixin
        '''
        yield from self.aliases.keys()

    def __contains__(self, alias):
        '''
        Implicit by __getitem__ (mixin) but implemented for performance reasons
        '''
        if isinstance(alias, Forest.Node):
            return alias in self.aliases.values()
        else:
            return alias in self.aliases

    def values(self):
        '''
        Implicit by __getitem__ (mixin) but implemented for performance reasons
        '''
        return self.aliases.values()

    def __len__(self):
        '''
        Note: number of keys (i.e. aliases) may be *less than* number of values (i.e. nodes)
        '''
        return len(self.aliases.values())

    def canopy(self):
        return (self.nodes.values() | self.trees) - self.nodes.keys()

    def height(self):
        '''
        Maximum height (of all nodes in Forest)
        '''
        return max(self.levels.values())

    def __str__(self):
        return '\n'.join([str(self.trees), str(self.nodes)])

    class Node():
        '''
        Store the (non-unique) alias and its (unique) ID for a Node
        '''
        def __init__(self, alias, id):
            self.alias = Forest.Node.deid(alias)
            self.id = id

        @staticmethod
        def deid(alias):
            return alias.alias if isinstance(alias, Forest.Node) else alias

        def offset(self, value):
            return Forest.Node(self.alias, self.id+value)

        def __hash__(self):
            return self.id

        def __lt__(self, other):
            return self.id < other.id

        def __eq__(self, other):
            return self.id == other.id

        def __str__(self):
            return '#' + str(self.id) + ':' + str(self.alias)

        def __repr__(self):
            return str(self)

        def identified(self,
                identified: bool, # return fullNode
                off: int=0,
            ):
            '''
            Return either an offset Node ID or simply the alias
            '''
            return self.offset(off) if identified else self.alias

    def sprout(self, alias):
        '''
        Make a unique node identifier referenced by an alias
        '''
        self.counter += 1
        return Forest.Node(alias, self.counter)

    def aliased(self, alias=None):
        '''
        Generate set of nodes referenced by alias
        '''
        for alias in self.trees if alias is None else {alias}:
            if isinstance(alias, Forest.Node):
                nodes = {alias} # single node
            elif alias in self.aliases:
                nodes = self.aliases[alias] # multiple nodes, maybe
            else:
                raise KeyError
            yield from nodes

    def above(self, alias):
        '''
        Generate nodes above node(s)
        '''
        for node in self.aliased(alias):
            if node in self.nodes:
                yield from self.nodes[node]

    def branches(self, alias):
        '''
        Return branches (e.g. Trees) above the node(s)
        '''
        for node in self.above(alias):
            yield self[node]

    def below(self, alias):
        '''
        Generate parent(s) below node(s)
        '''
        for node in self.aliased(alias):
            if node in ~self.nodes:
                yield (~self.nodes)[node]

    def root(self, alias=None):
        '''
        Return tree root(s) of alias
        '''
        for node in self.aliased(alias):
            if node in self.trees:
                yield node
            else:
                for lower in self.below(node):
                    yield from self.root(lower)

    def leaves(self, alias=None):
        '''
        Return leaves reachable from  alias
        '''
        for node in self.aliased(alias):
            if node not in self.nodes:
                yield node
            else:
                for upper in self.above(node):
                    yield from self.leaves(upper)

    def _add_node(self, alias):
        if isinstance(alias, Forest.Node): # already sprouted
            new = alias
            if alias.id > self.counter: # pre-offset
                self.counter = alias.id + 1
        else:
            new = self.sprout(alias)
        self.aliases[Forest.Node.deid(new)] = new
        return new

    def _add_twig(self, lower, upper):
        for node in self.aliased(lower):
            new = self._add_node(upper)
            self.nodes[node] = new
            self.levels[new] = self.levels[node]+1

    def _add_tree(self, tree):
        new = self._add_node(tree)
        self.trees.add(new)
        self.levels[new] = 0
        return new

    def climb(self,
            alias = None, # start here; when None start at tree roots
            level: bool = False, # include level in iterator
            twig: bool = False, # return connective (lower, upper) pair instead of just node
            identified: bool = True, # when True use full Node ID, when False just use aliases
            offset: int = 0, # add offset to node ID
        ):
        '''
        Generate tree of nodes reacheable from alias
        '''
        def idd(node):
            '''
            Just a shortcut, meaning: "Id'd"
            '''
            return node.identified(identified, offset)

        def token(lower, upper=None):
            if level:
                height = (self.levels[node],)
            else:
                height = ()
            if upper is None:
                return height + (idd(lower),)
            else:
                return height + (idd(lower), idd(upper))

        for node in self.aliased(alias):
            if not twig:
                yield token(node)
            if node in self.nodes:
                for other in self.nodes[node]:
                    if twig:
                        yield token(node, other)
                    yield from self.climb(other,
                        level = level,
                        twig = twig,
                        offset = offset,
                        identified = identified)

    def sorted(self,
            alias = None,
            level: bool = False,
            twig: bool = False,
            offset: int = 0,
            identified: bool = True,
        ):
        '''
        A topologically sorted node *list* (not iterator)
        '''
        nodes = list(
            self.climb(alias,
                level = True, # need this to topologically sort
                offset = offset,
                identified = identified,
                twig = twig))
        if not level: # but get rid of the level if not requested
            if twig:
                nodes = [(lower, upper) for lvl, lower, upper in nodes]
            else:
                nodes = [node for lvl, node in nodes]
        return sorted(nodes)

    @unfrozen
    def __delitem__(self, node):
        for level, node in reversed(self.sorted(node, level=True)):
            del self.levels[node]
            del (~self.aliases)[node]
            if node in self.nodes:
                del self.nodes[node]
            if node in self.trees:
                self.trees.remove(node)
            else: # has a parent
                del (~self.nodes)[node]

    @staticmethod
    def equals(forest1, forest2, tree1=None, tree2=None):
        def nodes(forest, tree):
            return forest.sorted(alias=tree, identified=False, level=True, twig=True)
        return nodes(forest1, tree1) == nodes(forest2, tree2)

    def __eq__(self, other):
        return Forest.equals(self, other)

    def cutting(self,
            alias = None,
            identified: bool = True,
            offset: int = 0,
            morph: types.FunctionType = Unindexed.identity, # modify keys/values upon entry
        ):
        '''
        Return subforest rooted at alias
        '''
        def morphed(node):
            if isinstance(node, Forest.Node):
                alias = morph(node.alias)
                return Forest.Node(alias,node.id) if alias is not None else None
            else:
                return morph(node)

        new = Forest(parent=self, offset=offset)
        for node in self.aliased(alias):
            tree = morphed(node.identified(identified, offset))
            if tree is not None:
                new._add_tree(tree)
                for lower, upper in self.climb(
                        node,
                        level=False,
                        identified=identified,
                        offset=offset,
                        twig=True):
                    lower, upper = morphed(lower), morphed(upper)
                    if lower is not None and upper is not None and lower in new:
                        new[lower] = upper
        return new

    def __getitem__(self, alias):
        return self.cutting(alias)

    def graft(self,
            forest,
            alias = None,
            identified: bool = True,
        ):
        '''
        Glue forest onto another forest at node(s)
        '''
        def grow(offset):
            for lower, upper in forest.sorted(
                    twig = True,
                    level = False,
                    offset = offset,
                    identified = identified):
                self._add_twig(lower, upper)

        if alias is not None: # graft to aliased nodes
            for node in self.aliased(alias):
                offset = self.counter # increase offset with each new node attachment
                for tree in forest.trees:
                    self._add_twig(node, tree.identified(identified, offset))
                grow(offset)
        else: # add as new rooted trees
            offset = self.counter
            for tree in forest.trees:
                self._add_tree(tree.identified(identified, offset))
            grow(offset)

    @unfrozen
    def __setitem__(self, lower, upper):
        if isinstance(upper, Forest):
            self.graft(
                alias = lower,
                forest = upper,
                identified = True)
        else:
            self._add_twig(lower, upper)

    @unfrozen
    def update(self, other):
        '''
        Perform set union when "other" is a Forest;
        otherwise, add a new tree

        Note: MutableMapping mixin
        '''
        if isinstance(other, Forest):
            self.graft(
                alias = None,
                forest = other,
                identified = True)
        else:
            self._add_tree(other)
        return self

    def subtract(self, other):
        '''
        Perform set difference when "other" is a Forest;
        otherwise, delete element

        Note: Encyclopedia mixin
        '''
        new = self.copy()
        if isinstance(other, Forest):
            for t1 in self.trees:
                for t2 in other.trees:
                    if self[t1] == other[t2] and t1 in new:
                        del new[t1]
        else:
            del new[other]
        return new

    def unique(self):
        '''
        Eliminate duplicate trees in a forest
        '''
        new = self.copy()
        trees = sorted(list(self.trees))
        remove=set()
        for i1, t1 in enumerate(trees):
            for t2 in trees[i1+1:]:
                if self[t1] == self[t2]:
                    remove.add(t2)
        for tree in remove:
            del new[tree]
        return new

    def compose(self, other):
        '''
        Composition depends on context of "other":

        - Scaled by integers
        - Acted upon by functions
        - Grafted with Forests
        '''
        new = self.copy()
        if isinstance(other, int):
            for dupe in range(other-1):
                new += self.copy()
        elif isinstance(other, types.FunctionType):
            return self.cutting(morph = other)
        elif isinstance(other, Forest):
            for tree in other.trees:
                if tree.alias in self:
                    for node in self.aliased(tree.alias):
                        for branch in other.branches(tree):
                            new[node] = branch
        else:
            assert False
        return new

    @staticmethod
    def node2alias(generator):
        aliases = {node.alias for node in generator}
        if len(aliases) == 0:
            return {}
        elif len(aliases) == 1:
            return aliases.pop()
        else:
            return aliases
