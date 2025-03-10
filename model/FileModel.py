class FileModel:
    def __init__(self, item_label: str, item_value: str):
        self.item_label = item_label
        self.item_value = item_value
        self.processed = False

    def __call__(self, *args, **kwargs):
        return self.item_value, self.item_label

    def get_item_value(self):
        return self.item_value
    def get_item_label(self):
        return self.item_label