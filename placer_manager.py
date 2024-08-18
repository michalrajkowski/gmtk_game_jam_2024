class PlacerManager:
    def __init__(self) -> None:
        self.placing_mode = False
        self.placing_object = None

    def reset(self):
        self.placing_mode = False
        self.placing_object = None