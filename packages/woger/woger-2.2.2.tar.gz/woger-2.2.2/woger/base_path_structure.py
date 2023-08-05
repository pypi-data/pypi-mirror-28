from pathlib import Path
from typing import Union

import os

from .workspace_meta import PathStructureMeta


class BasePathStructure(metaclass=PathStructureMeta):
    def __init__(self, root: Union[bytes, str]):
        """Base class for path structure

        Parameters
        ----------
        root: path-like
            Path structure root


        Examples
        --------

        :ref:`basic-path-structure`

        """
        self._root = Path(root)
        os.makedirs(str(self._root), exist_ok=True)
