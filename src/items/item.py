class Item:
    def __init__(self, name, description, image_path):
        self.name = name
        self.description = description
        self.iid = 1 # TODO: look for id in db
        self.image_path = image_path