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
                             int(Player.config["Tilemap"]["tile_width"]) * 0,
                             int(Player.config["Tilemap"]["tile_height"]),
                             int(Player.config["Tilemap"]["player_width"]),
                             int(Player.config["Tilemap"]["player_height"])))
        self.respawn_pos = None
        self.next_level = False
        self.true_coords = list(self.rect.topleft)

    def moveUp(self):
        self.true_coords[1] -= float(Player.config["Player"]["speed"])
        self.rect.y = self.true_coords[1]

    def moveDown(self):
        self.true_coords[1] += float(Player.config["Player"]["speed"])
        self.rect.y = self.true_coords[1]

    def moveLeft(self):
        self.true_coords[0] -= float(Player.config["Player"]["speed"])
        self.rect.x = self.true_coords[0]

    def moveRight(self):
        self.true_coords[0] += float(Player.config["Player"]["speed"])
        self.rect.x = self.true_coords[0]

    def update(self, checkpoints: list[pygame.Rect], finish_tiles: list[pygame.Rect], coins: pygame.sprite.Group):
        for i in checkpoints:
            if i.colliderect(self): self.respawn_pos = i.center
        self.next_level = not self.rect.collidelist(finish_tiles) and not coins.sprites()


class Enemy(Gameobject):
    """
    color=0 → blue enemy
    color=1 → pink enemy
    color=2 → red enemy
    """
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, init_pos: tuple, key_positions: list[tuple[int, int]], movement_type: str, color: int, speed: float):
        super().__init__(init_pos,
                         image=pygame.image.load(Player.config["Tilemap"]["tilemap_path"]).convert_alpha().subsurface(
                             int(Player.config["Tilemap"]["player_width"]) + int(Player.config["Tilemap"]["coin_and_enemy_width"]) * color,
                             int(Player.config["Tilemap"]["tile_height"]),
                             int(Player.config["Tilemap"]["coin_and_enemy_width"]),
                             int(Player.config["Tilemap"]["coin_and_enemy_height"])))
        self.speed = speed
        self.key_positions = key_positions
        self.state = 0
        self.movement_type = movement_type
        self.true_coords = list(self.rect.topleft)

    def fromTo(self):
        next_state = (self.state + 1) % len(self.key_positions)
        if self.key_positions[self.state][0] == self.key_positions[next_state][0]:
            if self.key_positions[self.state][1] < self.key_positions[next_state][1]:
                self.true_coords[1] += self.speed
                self.rect.y = self.true_coords[1]
            elif self.key_positions[self.state][1] > self.key_positions[next_state][1]:
                self.true_coords[1] -= self.speed
                self.rect.y = self.true_coords[1]
        elif self.key_positions[self.state][1] == self.key_positions[next_state][1]:
            if self.key_positions[self.state][0] < self.key_positions[next_state][0]:
                self.true_coords[0] += self.speed
                self.rect.x = self.true_coords[0]
            elif self.key_positions[self.state][0] > self.key_positions[next_state][0]:
                self.true_coords[0] -= self.speed
                self.rect.x = self.true_coords[0]
        if self.rect.center == self.key_positions[next_state]:
            self.state = next_state

    def around(self):
        pass

    def update(self):
        match self.movement_type:
            case "from_to": self.fromTo()
            case "around": self.around()


class Coin(Gameobject):
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, xy: tuple[int, int]):
        super().__init__(xy,
                         image=pygame.image.load(Player.config["Tilemap"]["tilemap_path"]).convert_alpha().subsurface(
                             int(Player.config["Tilemap"]["player_width"]) + int(Player.config["Tilemap"]["coin_and_enemy_width"]) * 3,
                             int(Player.config["Tilemap"]["tile_height"]),
                             int(Player.config["Tilemap"]["coin_and_enemy_width"]),
                             int(Player.config["Tilemap"]["coin_and_enemy_height"])))
