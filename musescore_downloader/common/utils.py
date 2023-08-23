from argparse import Namespace

from ..managers.path_manager import PathManager

def initialize_vars(
    arguments: Namespace
):
    path_manager = PathManager()
    