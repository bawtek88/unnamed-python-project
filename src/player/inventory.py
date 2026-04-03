from items.item import Item
from items.weapon import Weapon

from collections import deque

class Inventory:
    def __init__(self, capacity):
        self.inventory: deque[Item] = deque(maxlen=capacity)
        self.toolbar: deque[Weapon] = deque(maxlen=3)
        self.accessories: deque[Item] = deque(maxlen=5)
        self.cyber_mods: list[Item] = []
        
        self.helmet: Item = None
        self.chest_piece: Item = None
        self.boots: Item = None
        
        