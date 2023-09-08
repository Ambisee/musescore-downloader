from .base_help import BaseHelp

class HelpMessage(BaseHelp):
    def __init__(self, message: str):
        self.message: str = message

    def get_help_content(self):
        return self.message

    def print(self, indent):
        print(indent * "\t" + f"- {self.message}")
