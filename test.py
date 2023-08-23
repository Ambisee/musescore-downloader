from musescore_downloader.core.initializers import handle_args
from argparse import Namespace


args: Namespace = handle_args()
print(args.__dict__)