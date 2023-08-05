'''
An Encyclopedia is an abstract container intended for smallish data sets which provides many of
the benefits of a relational (and non-relational) database but with lower syntactic friction.
'''

__version__ = '0.2'

from .templates import Unindexed,Indexed,Unity,Signed,Zero
from .relate import Relation
from .forest import Forest