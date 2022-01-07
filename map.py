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
                    self.coins_coords.append(Map.normalizeCoords(*dynamic[i]["tile_pos"]))
                elif dynamic[i]["type"] == "enemy":
                    dic = {"init_pos": Map.normalizeCoords(*dynamic[i]["init_pos"]),
                           "movement_type": dynamic[i]["movement_type"],
                           "color": dynamic[i]["color"],
                           "speed": dynamic[i]["speed"]}
                    match dynamic[i]["movement_type"]:
                        case "from_to":
                            dic["key_positions"] = [Map.normalizeCoords(*j) for j in dynamic[i]["key_positions"]]
                        case "around":
                            dic["circle_center"] = Map.normalizeCoords(*dynamic[i]["circle_center"])
                    self.enemies_data.append(dic)

    def generateSurface(self) -> pygame.Surface:
        tile_height, tile_width = int(Map.config["Tilemap"]["tile_height"]), int(Map.config["Tilemap"]["tile_width"])
        res = pygame.Surface((tile_width * self.map_width, tile_height * self.map_height))
        res.fill([int(i) for i in Map.config["Colors"]["background"].split(", ")])
        for row_index in range(self.map_height):
            for column_index in range(self.map_width):
                match int(self.static_map[row_index][column_index]):
                    case 0:
                        self.walls_tiles.append(pygame.Rect(*Map.normalizeCoords(column_index, row_index), tile_width, tile_height))
                    case 1:
                        if row_index % 2 == column_index % 2:
                            res.blit(self.tileset.subsurface(tile_width, 0, tile_width, tile_height), Map.normalizeCoords(column_index, row_index))
                        else:
                            res.blit(self.tileset.subsurface(tile_width * 2, 0, tile_width, tile_height), Map.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                    case 2:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height), Map.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        self.checkpoint_tiles.append(pygame.Rect(*Map.normalizeCoords(column_index, row_index), tile_width, tile_height))
                    case 3:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height), Map.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        self.spawn_tile = pygame.Rect(*Map.normalizeCoords(column_index, row_index), tile_width, tile_height)
                    case 4:
                        res.blit(self.tileset.subsurface(tile_width * 0, 0, tile_width, tile_height), Map.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(res, self.static_map, row_index, column_index)
                        self.finish_tiles.append(pygame.Rect(*Map.normalizeCoords(column_index, row_index), tile_width, tile_height))
        return res

    @staticmethod
    def normalizeCoords(x: int | float, y: int | float) -> tuple[float, float] | tuple[int, int]:
        return x * int(Map.config["Tilemap"]["tile_width"]), y * int(Map.config["Tilemap"]["tile_height"])

    @staticmethod
    def drawLineIfThereIsWall(res: pygame.Surface, static_map: list, row_index: int, column_index: int):
        BLACK = list(map(int, Map.config["Colors"]["black"].split(", ")))
        if static_map[row_index - 1][column_index] == "0":  # Top
            pygame.draw.line(res, BLACK, Map.normalizeCoords(column_index, row_index), Map.normalizeCoords(column_index + 1, row_index), 3)
        if static_map[row_index][column_index - 1] == "0":  # Left
            pygame.draw.line(res, BLACK, Map.normalizeCoords(column_index, row_index), Map.normalizeCoords(column_index, row_index + 1), 3)
        if static_map[row_index + 1][column_index] == "0":  # Bottom
            pygame.draw.line(res, BLACK, Map.normalizeCoords(column_index, row_index + 1), Map.normalizeCoords(column_index + 1, row_index + 1), 3)
        if static_map[row_index][column_index + 1] == "0":  # Right
            pygame.draw.line(res, BLACK, Map.normalizeCoords(column_index + 1, row_index), Map.normalizeCoords(column_index + 1, row_index + 1), 3)
