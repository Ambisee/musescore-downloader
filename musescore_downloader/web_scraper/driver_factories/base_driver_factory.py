class BaseDriverFactory:
    def __init__(self, *args, **kwargs):
        self.headless = kwargs.get("headless", True)

    def create_driver(self):
        pass