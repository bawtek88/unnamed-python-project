from .item import Item

class Weapon(Item):
    def __init__(self, name, description, image_path, damage):
        super().__init__(name, description, image_path)
        self.damage = damage