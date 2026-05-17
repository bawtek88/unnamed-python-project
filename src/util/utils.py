import pygame
import os
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
OBJECTS_DIR = PROJECT_ROOT / "src" / "objects"
LEVELS_DIR = PROJECT_ROOT / "src"/ "util" / "levels" #could restructure it later

class ImageLoader:
    def __init__(self):
        self.images = {}
        image_path = ASSETS_DIR / "no_texture.png"
        self.missing_image = pygame.image.load(image_path)

    def load_image(self, name, filename):
        try:
            image_path = ASSETS_DIR / filename
            self.images[name] = pygame.image.load(image_path).convert_alpha()
        except Exception as e:
            print(f"Warning: Image '{name}' in '{filename}' is missing. Using missing texture placeholder. Error: {e}")
            self.images[name] = self.missing_image
         

    def get_image(self, name):
        image = self.images.get(name)
        if image is None:
            print(f"Warning: Image '{name}' not found. Using missing texture placeholder.")
            return self.missing_image
        return image
class WorldObject(pygame.sprite.Sprite):
    def __init__(self, position, image, object_data):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        self.name = object_data.get("name", "unknown")
        self.type = object_data.get("type", self.name)
        self.has_collision = object_data.get("has_collision", False)
        self.collision_data = object_data.get("collision", None)

        self.collision_rect = None
        self.create_collision_rect()

    def create_collision_rect(self):
        if not self.has_collision or self.collision_data is None:
            return

        if self.collision_data.get("type") == "rect":
            offset_x, offset_y = self.collision_data.get("offset", [0, 0])
            width, height = self.collision_data.get("size", [self.rect.width, self.rect.height])

            self.collision_rect = pygame.Rect(
                self.rect.x + offset_x,
                self.rect.y + offset_y,
                width,
                height
            )

    def update(self):
        if self.collision_rect is not None:
            offset_x, offset_y = self.collision_data.get("offset", [0, 0])
            self.collision_rect.x = self.rect.x + offset_x
            self.collision_rect.y = self.rect.y + offset_y

class LevelLoader:
    def __init__(self, image_loader):
        self.image_loader = image_loader
        self.current_level = None 

    def load_level(self, level_name):
        #should add some safecheck
        level_path = LEVELS_DIR / f"{level_name}.json"

        with open(level_path, "r") as file:
            level_data = json.load(file)
        background_name = level_data["background"]
        self.image_loader.load_image(background_name, background_name)
        level_size = tuple(level_data.get("size", [0, 0]))
        spawn = tuple(level_data.get("spawn", [0,0]))

        objects = []

        for object in level_data.get("objects", []):
            object_type = object["type"]
            position = tuple(object.get("position", [0,0]))

            object_data = self.load_object_data(object_type)
            sprite_filename = object_data["sprite"]
            self.image_loader.load_image(object_type, sprite_filename)

            game_object = {
                "type": object_type,
                "name": object_data["name"],
                "position": position,
                "sprite": object_type,
                "has_collision": object_data.get("hasCollision", False),
                "collision": object_data.get("collision", None)
            }
            objects.append(game_object)
        self.current_level = {
            "name": level_name,
            "background": background_name,
            "size": level_size,
            "spawn": spawn,
            "objects": objects
        }
        return self.current_level

    def load_object_data(self, object_name):
        object_path = OBJECTS_DIR / f"{object_name}.json"
        with open(object_path, "r") as file:
            return json.load(file)

    def get_level(self):
        return self.current_level

    