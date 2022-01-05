import pygame
from configparser import ConfigParser
from json import load


class Map:
    """
    Types of tiles:
    0: Wall
    1: Not wall
    2: Checkpoint
    3: Start
    4: Finish
    """
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, map_number: int):
        self.tileset = pygame.image.load(Map.config["Tilemap"]["tilemap_path"]).convert_alpha()
        self.map_number = map_number
        self.dynamic_map = []
        self.walls_tiles = []
        self.spawn_tile = None
        self.checkpoint_tiles = []
        self.finish_tiles = []
        self.coins_coords = []
        self.enemies_data = []
        self.static_map = []
        self.map_width, self.map_height = None, None
        self.parseMap()

    def parseMap(self):
        with open(f"maps/MAP{'0' * (self.map_number < 10)}{self.map_number}-static.map", "r") as static:
            self.map_width, self.map_height = map(int, static.readline().split("x"))
            for _ in range(self.map_height):
                self.static_map.append(static.readline().split())
        with open(f"maps/MAP{'0' * (self.map_number < 10)}{self.map_number}-dynamic.json", "r") as raw_dynamic:
            dynamic = load(raw_dynamic)
            for i in dynamic.keys():
                if dynamic[i]["type"] == "coin":
                    self.coins_coords.append((dynamic[i]["tile_pos"][0] * int(Map.config["Tilemap"]["tile_width"]),
                                              dynamic[i]["tile_pos"][1] * int(Map.config["Tilemap"]["tile_height"])))
                elif dynamic[i]["type"] == "enemy":
                    self.enemies_data.append(
                        {"init_pos": (dynamic[i]["init_pos"][0] * int(Map.config["Tilemap"]["tile_width"]),
                                      dynamic[i]["init_pos"][1] * int(Map.config["Tilemap"]["tile_height"])),
                         "key_positions": [(j[0] * int(Map.config["Tilemap"]["tile_width"]),
                                            j[1] * int(Map.config["Tilemap"]["tile_height"])) for j in dynamic[i]["key_positions"]],
                         "movement_type": dynamic[i]["movement_type"],
                         "color": dynamic[i]["color"],
                         "speed": dynamic[i]["speed"]})

    def generateSurface(self) -> pygame.Surface:
        res = pygame.Surface((int(Map.config["Tilemap"]["tile_width"]) * self.map_width, int(Map.config["Tilemap"]["tile_height"]) * self.map_height))
        res.fill(list(map(int, Map.config["Colors"]["background"].split(", "))))
        tile_height, tile_width = int(Map.config["Tilemap"]["tile_height"]), int(Map.config["Tilemap"]["tile_width"])
        for row_index in range(self.map_height):
            for column_index in range(self.map_width):
                match int(self.static_map[row_index][column_index]):
                    case 0:
                        self.walls_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                            tile_width, tile_height))
                    case 1:
                        if row_index % 2 == column_index % 2:
                            res.blit(self.tileset.subsurface(tile_width, 0, tile_width, tile_height),
                                     (tile_width * column_index, tile_height * row_index))
                        else:
                            res.blit(self.tileset.subsurface(tile_width * 2, 0, tile_width, tile_height),
                                     (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                    case 2:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height),
                                 (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        self.checkpoint_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                                 tile_width, tile_height))
                    case 3:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height),
                                 (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        self.spawn_tile = pygame.Rect(tile_width * column_index, tile_height * row_index, tile_width,
                                                      tile_height)
                    case 4:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height),
                                 (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        self.finish_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                             tile_width, tile_height))
        return res

    @classmethod
    def drawLineIfThereIsWall(cls, res: pygame.Surface, static_map: list, row_index: int, column_index: int):
        tile_width, tile_height = int(cls.config["Tilemap"]["tile_width"]), int(cls.config["Tilemap"]["tile_height"])
        BLACK = list(map(int, cls.config["Colors"]["black"].split(", ")))
        if static_map[row_index - 1][column_index] == "0":  # Top
            pygame.draw.line(res, BLACK, (tile_width * column_index, tile_height * row_index),
                             (tile_width * (column_index + 1), tile_height * row_index), 3)
        if static_map[row_index][column_index - 1] == "0":  # Left
            pygame.draw.line(res, BLACK, (tile_width * column_index, tile_height * row_index),
                             (tile_width * column_index, tile_height * (row_index + 1)), 3)
        if static_map[row_index + 1][column_index] == "0":  # Bottom
            pygame.draw.line(res, BLACK, (tile_width * column_index, tile_height * (row_index + 1)),
                             (tile_width * (column_index + 1), tile_height * (row_index + 1)), 3)
        if static_map[row_index][column_index + 1] == "0":  # Right
            pygame.draw.line(res, BLACK, (tile_width * (column_index + 1), tile_height * row_index),
                             (tile_width * (column_index + 1), tile_height * (row_index + 1)), 3)
