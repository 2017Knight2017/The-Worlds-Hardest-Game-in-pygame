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

    Enemy data standard: [id: str,
                          type: from_to | circle,
                          begin_x: int, begin_y: int,
                          end_x: int, end_y: int,
                          speed: int]
    """
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self, map_number: int):
        self.tileset = pygame.image.load(Map.config["Tilemap"]["tilemap_path"]).convert_alpha()
        self.map_number = map_number
        self.spawn = 4
        self.checkpoints = []
        self.finish_tiles = []
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
        res.fill((216, 194, 255))
        tile_height, tile_width = int(Map.config["Tilemap"]["tile_height"]), int(Map.config["Tilemap"]["tile_width"])
        for row_index in range(self.height):
            for column_index in range(self.width):
                match int(self.static_map[row_index][column_index]):
                    case 1:
                        if row_index % 2 == column_index % 2:
                            res.blit(self.tileset.subsurface(tile_width, 0, tile_width, tile_height),
                                     (tile_width * column_index, tile_height * row_index))
                        else:
                            res.blit(self.tileset.subsurface(tile_width * 2, 0, tile_width, tile_height),
                                     (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                    case 2 | 3 | 4:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height),
                                 (tile_width * column_index, tile_height * row_index))
                        Map.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                    case 2:
                        self.checkpoints.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                            tile_width, tile_height))
                    case 3:
                        self.spawn = (tile_width * column_index, tile_height * row_index)
                    case 4:
                        self.finish_tiles.append(pygame.Rect(tile_width * column_index, tile_height * row_index,
                                                             tile_width, tile_height))
        return res

    @staticmethod
    def drawLineIfThereIsWall(res, static_map, row_index, column_index):
        if static_map[row_index - 1][column_index] == "0":  # Top
            pygame.draw.line(res, (0, 0, 0), (20 * column_index, 20 * row_index),
                             (20 * (column_index + 1), 20 * row_index), 2)
        if static_map[row_index][column_index - 1] == "0":  # Left
            pygame.draw.line(res, (0, 0, 0), (20 * column_index, 20 * row_index),
                             (20 * column_index, 20 * (row_index + 1)), 2)
        if static_map[row_index + 1][column_index] == "0":  # Bottom
            pygame.draw.line(res, (0, 0, 0), (20 * column_index, 20 * (row_index + 1)),
                             (20 * (column_index + 1), 20 * (row_index + 1)), 2)
        if static_map[row_index][column_index + 1] == "0":  # Right
            pygame.draw.line(res, (0, 0, 0), (20 * (column_index + 1), 20 * row_index),
                             (20 * (column_index + 1), 20 * (row_index + 1)), 2)
