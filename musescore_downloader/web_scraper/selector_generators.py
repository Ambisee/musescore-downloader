class SelectorGenerators:
    """Collection of functions that generates CSS selectors
    """

    @staticmethod
    def generate_id_selector(id: str):
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
    def generate_class_selector(class_name: str):
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
