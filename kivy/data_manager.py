class DataManager:
    def __init__(self):
        self.images = []

    def add_images(self, paths):
        self.images.extend(paths)

    def remove_image(self, path):
        if path in self.images:
            self.images.remove(path)

    def get_images(self):
        return self.images
