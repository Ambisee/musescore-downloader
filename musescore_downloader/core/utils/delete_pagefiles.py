import os
from concurrent.futures import ThreadPoolExecutor

from ...common.types.save_complete_object import SaveCompleteObject

def delete_pagefiles(file_infos: list[SaveCompleteObject]) -> None:
    parent_dir = os.path.dirname(file_infos[0].path)

    with ThreadPoolExecutor() as executor:
        for info in file_infos:
            executor.submit(os.remove, info.path)

    with os.scandir(parent_dir) as it:
        if not any(it):
            os.rmdir(parent_dir)
    
    return