import pygame
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

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
    