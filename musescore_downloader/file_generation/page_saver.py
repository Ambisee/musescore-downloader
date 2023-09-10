import os
import logging
from typing import Literal
from concurrent.futures import (
    ThreadPoolExecutor, 
    Future, 
    wait
)

from ..common.constants import content_type_to_extension
from ..common.types import ContentObject, SaveCompleteObject
from ..managers import PathManager

class PageSaver:
    """Saves the binary data of the pages into separate files.

    Attributes
    ----------
    title : str
        The title of the music sheet.
    content_objects : list[ContentObject]
        Collection of objects that contains the binary data of each pages.
    path_manager : PathManager
        Object that manages the output paths.
    """
    def __init__(
        self, 
        title: str,
        content_objects: list[ContentObject],
        path_manager: PathManager
    ) -> None:
        self.title: str = title
        self.content_objects: list[ContentObject] = content_objects
        self.path_manager: PathManager = path_manager

    def ensure_dir_exists(self) -> dict[Literal["created_path", "path"], bool | str]:
        """Checks if the page files directory exists and creates one if it doesn't.

        Returns
        -------
        result : dict with str keys and bool or str values
            dictionary containing the path to the page files dir and a value indicating
            whether or not the directory is created. The dictionary contains the following
            key-value pairs:
            - created_path : bool = indicates whether a new directory is created or not.
            - path : str = the path to the page files directory
        """
        target_path = self.path_manager.get_page_image_dir(self.title)
        result = {"created_path": True, "path": target_path}

        if not os.path.isdir(target_path):
            os.makedirs(target_path)
            return result
    
        result["created_path"] = False
        return result

    def save_page(self, content_obj: ContentObject) -> SaveCompleteObject:
        """Saves the content of a page to a file.

        Parameters
        ----------
        content_obj : ContentObject
            Object that holds the string content of a page file and some metadata.
        
        Returns
        -------
        SaveCompleteObject
            Object that holds data about the generated file.
        """
        path = self.path_manager.get_page_image_filepath(
            content_obj.page_num, 
            content_obj.title,
            content_type_to_extension[content_obj.content_type]
        )
        
        with open(
            path,
            "wb"
        ) as f:
            f.write(content_obj.content)

        return SaveCompleteObject(
            path,
            content_obj.page_num,
            content_type_to_extension[content_obj.content_type]
        )

    def download_callback(self, task: Future[SaveCompleteObject]) -> None:
        """Callback function when the process of saving the page content
        is complete

        Parameters
        ----------
        task : Future that returns a SaveCompleteObject
            The thread process that downloads a page content to a file.
        
        Returns
        -------
        None
        """
        logging.info(f"Finished saving page {task.result().page_num}.")

    def execute(self) -> list[SaveCompleteObject]:
        """Executes the process.

        Returns
        -------
        list of SaveCompleteObject
        
        Raises
        ------
        KeyError
            A page is retrieved with an unforeseen content type, which leads
            to no file extension that can be used to represent the page file.
        """
        logging.info("Start saving pages of the music sheet into files...")
        
        logging.info("Ensuring save directory exists...")

        ensure_dir_res = self.ensure_dir_exists()
        if ensure_dir_res['created_path']:
            logging.warning(f"Created the target directory: {ensure_dir_res['path']}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks: list[Future[SaveCompleteObject]] = []

            for i, content_obj in enumerate(self.content_objects):
                logging.info(f"Saving contents of page {int(i) + 1}...")

                task = executor.submit(self.save_page, content_obj)
                task.add_done_callback(self.download_callback)

                tasks.append(task)
            
        result: list[SaveCompleteObject] = []

        for task in tasks:
            if task.exception():
                raise task.exception()
            result.append(task.result())

        return result
