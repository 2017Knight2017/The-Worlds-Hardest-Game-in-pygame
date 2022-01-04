import pygame
from configparser import ConfigParser


class Gameobject(pygame.sprite.Sprite):
    def __init__(self, xy: tuple[int, int], filename="", image=None):
        pygame.sprite.Sprite.__init__(self)
        if filename:
            self.image = image.load(filename).convert_alpha()
        elif image:
            self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=(xy[0], xy[1]))


class Player(Gameobject):
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, spawn_tile_xy: tuple[int, int]):
        super().__init__(spawn_tile_xy,
                         image=pygame.image.load(Player.config["Tilemap"]["tilemap_path"]).convert_alpha().subsurface(
                             int(Player.config["Tilemap"]["sprite_width"]) * 0,
                             int(Player.config["Tilemap"]["tile_height"]),
                             int(Player.config["Tilemap"]["sprite_width"]),
                             int(Player.config["Tilemap"]["sprite_height"])))
        self.respawn_pos = None
        self.next_level = False

    def moveUp(self):
        self.rect.y -= int(Player.config["Player"]["speed"])

    def moveDown(self):
        self.rect.y += int(Player.config["Player"]["speed"])

    def moveLeft(self):
        self.rect.x -= int(Player.config["Player"]["speed"])

    def moveRight(self):
        self.rect.x += int(Player.config["Player"]["speed"])

    def update(self, checkpoints: list[pygame.Rect], finish_tiles: list[pygame.Rect], coins: pygame.sprite.Group):
        for i in checkpoints:
            if i.colliderect(self): self.respawn_pos = i.center
        self.next_level = not self.rect.collidelist(finish_tiles) and not coins.sprites()


class Enemy(Gameobject):
    """
    color=1 → blue enemy
    color=2 → pink enemy
    color=3 → red enemy
    """
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, xy: tuple[int, int], color: int = 1):
        super().__init__(xy,
                         image=pygame.image.load(Player.config["Tilemap"]["tilemap_path"]).convert_alpha().subsurface(
                             int(Player.config["Tilemap"]["sprite_width"]) * color,
                             int(Player.config["Tilemap"]["tile_height"]),
                             int(Player.config["Tilemap"]["sprite_width"]),
                             int(Player.config["Tilemap"]["sprite_height"])))


class Coin(Gameobject):
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, xy: tuple[int, int]):
        super().__init__(xy,
                         image=pygame.image.load(Player.config["Tilemap"]["tilemap_path"]).convert_alpha().subsurface(
                             int(Player.config["Tilemap"]["sprite_width"]) * 4,
                             int(Player.config["Tilemap"]["tile_height"]),
                             int(Player.config["Tilemap"]["sprite_width"]),
                             int(Player.config["Tilemap"]["sprite_height"])))
