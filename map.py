import pygame
from configparser import ConfigParser


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
        self.static_map = []
        self.width, self.height = None, None
        self.parseMap()

    def parseMap(self):
        with open(f"maps/MAP{'0' * (self.map_number < 10)}{self.map_number}-static.map", "r") as static:
            self.width, self.height = map(int, static.readline().split("x"))
            for i in range(self.height):
                self.static_map.append(static.readline().split())
        with open(f"maps/MAP{'0' * (self.map_number < 10)}{self.map_number}-dynamic.map", "r") as dynamic:
            for i in dynamic:
                arr = i.split(", ")
                self.dynamic_map.append({
                    "id": arr[0],
                    "type": arr[1],
                    "begin_pos": (int(arr[2]), int(arr[3])),
                    "end_pos": (int(arr[4]), int(arr[5])),
                    "speed": int(arr[6])
                })

    def generateSurface(self) -> pygame.Surface:
        res = pygame.Surface((20 * (self.width + 10), 20 * (self.height + 10)))
        walls_tiles, checkpoint_tiles, finish_tiles, spawn_tile = [], [], [], None
        res.fill((216, 194, 255))
        tile_height, tile_width = int(Map.config["Tilemap"]["tile_height"]), int(Map.config["Tilemap"]["tile_width"])
        for row_index in range(self.height):
            for column_index in range(self.width):
                match int(self.static_map[row_index][column_index]):
                    case 0:
                        walls_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
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
                        checkpoint_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                            tile_width, tile_height))
                    case 3:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height),
                                 (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        spawn_tile = pygame.Rect(tile_width * column_index, tile_height * row_index, tile_width,
                                                 tile_height)
                    case 4:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height),
                                 (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        finish_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                        tile_width, tile_height))
        return res, walls_tiles, spawn_tile, checkpoint_tiles, finish_tiles

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
