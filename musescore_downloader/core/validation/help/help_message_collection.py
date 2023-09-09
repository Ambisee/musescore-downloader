from .base_help import BaseHelp

class HelpMessageCollection(BaseHelp):
    def __init__(self, message: str, help_collection: list[BaseHelp]):
        self.message: str = message
        self.help_collection: list[BaseHelp] = help_collection
    
    def add_help(self, help: BaseHelp):
        self.help_collection.append(help)

    def get_help_content(self):
        result = []

        for help in self.help_collection:
            result.append(help.get_help_content())
        
        return result

    def print(self, indent):
        print(indent * "\t" + f"- {self.message}")        
        for help in self.help_collection:
            help.print(indent + 1)
