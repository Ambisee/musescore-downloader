class SelectorsManager:
    """Collection of functions that generates CSS selectors
    """

    @staticmethod
    def generate_id_selector(id: str) -> str:
        """Generates a CSS selector based on an HTML element's `id` attribute

        Parameters
        ----------
        id : str
            The `id` value of the targeted HTML element.
        
        Returns
        -------
        str
            String representation of a CSS selector.
        """
        return f"#{id}"

    @staticmethod
    def generate_class_selector(class_name: str) -> str:
        """Generates a CSS selector based on an HTML element's `class` attribute

        Parameters
        ----------
        class_name : str
            The `class` value of the targeted HTML element. Must be whitespace-separated if 
            element has multiple classes.
        
        Returns
        -------
        str
            String representation of a CSS selector.
        """
        class_list = class_name.split(" ")
        return "." + ".".join(class_list)

    def __init__(
        self,
        scroll_element_id: str,
        page_container_class: str,
        total_pages_container_class: str,
        title_container_class: str
    ) -> None:
        self.set_scroll_element_selector(scroll_element_id)
        self.set_page_container_selector(page_container_class)
        self.set_total_pages_container_selector(total_pages_container_class)
        self.set_title_container_class(title_container_class)

    def set_scroll_element_selector(self, scroll_element_id: str) -> None:
        self.scroll_element_selector = self.generate_id_selector(scroll_element_id)

    def set_page_container_selector(self, page_container_class: str) -> None:
        self.page_container_selector = self.generate_class_selector(page_container_class)
    
    def set_total_pages_container_selector(self, total_pages_container_class: str) -> None:
        self.total_pages_container_selector = self.generate_class_selector(total_pages_container_class)
    
    def set_title_container_class(self, title_container_class: str) -> None:
        self.title_container_selector = self.generate_class_selector(title_container_class)
