from typing      import TYPE_CHECKING

from .node       import Node
from .data       import get_definitions
from .tagfile    import Tagfile
from .definition import Definition

if TYPE_CHECKING:
    from .nodes  import *
