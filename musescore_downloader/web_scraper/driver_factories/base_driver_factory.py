class BaseDriverFactory:
    def __init__(self, *args, **kwargs):
        self.headless = kwargs.get("headless", True)
        self.create_driver()

    def create_driver(self):
        pass