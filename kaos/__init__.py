from typing   import TYPE_CHECKING

from .data    import get_definitions
from .tagfile import Node
from .tagfile import Tagfile
from .tagfile import Definition

if TYPE_CHECKING:
    from .nodes  import *
