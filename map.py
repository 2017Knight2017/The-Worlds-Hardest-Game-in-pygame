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
        self.map_tile_width, self.map_tile_height = None, None
        self.map_pixel_width, self.map_pixel_height = None, None
        self.tile_pixel_width, self.tile_pixel_height = int(Map.config["Tilemap"]["tile_width"]), int(Map.config["Tilemap"]["tile_width"])
        self.parseMap()

    def parseMap(self):
        map_name = f"MAP{'0' * (self.map_number < 10)}{self.map_number}"
        with open(f"maps/{map_name}/{map_name}-static.map", "r") as static_map:
            self.map_tile_width, self.map_tile_height = map(int, static_map.readline().split("x"))
            self.map_pixel_width, self.map_pixel_height = self.tile_pixel_width * self.map_tile_width, self.tile_pixel_height * self.map_tile_height
            for _ in range(self.map_tile_height):
                self.static_map.append(static_map.readline().split())
        with open(f"maps/{map_name}/{map_name}-dynamic.json", "r") as raw_dynamic_map:
            dynamic_map = load(raw_dynamic_map)
            for i in dynamic_map.keys():
                if dynamic_map[i]["type"] == "coin":
                    self.coins_coords.append(self.normalizeCoords(*dynamic_map[i]["tile_pos"], dynamic=True))
                elif dynamic_map[i]["type"] == "enemy":
                    dic = {"init_pos": self.normalizeCoords(*dynamic_map[i]["init_pos"], dynamic=True),
                           "movement_type": dynamic_map[i]["movement_type"],
                           "color": dynamic_map[i]["color"],
                           "speed": dynamic_map[i]["speed"]}
                    match dynamic_map[i]["movement_type"]:
                        case "from_to":
                            dic["key_positions"] = [self.normalizeCoords(*j, dynamic=True) for j in dynamic_map[i]["key_positions"]]
                        case "around":
                            dic["circle_center"] = self.normalizeCoords(*dynamic_map[i]["circle_center"], dynamic=True)
                            dic["clockwise"] = dynamic_map[i]["clockwise"]
                    self.enemies_data.append(dic)

    def generateSurface(self) -> pygame.Surface:
        surface = pygame.Surface((self.map_pixel_width, self.map_pixel_height))
        surface.fill([int(i) for i in Map.config["Colors"]["background"].split(", ")])
        for row_index in range(self.map_tile_height):
            for column_index in range(self.map_tile_width):
                match int(self.static_map[row_index][column_index]):
                    case 0:
                        self.walls_tiles.append(pygame.Rect(*self.normalizeCoords(column_index, row_index, dynamic=True), self.tile_pixel_width, self.tile_pixel_height))
                    case 1:
                        if row_index % 2 == column_index % 2:
                            surface.blit(self.tileset.subsurface(self.tile_pixel_width, 0, self.tile_pixel_width, self.tile_pixel_height), self.normalizeCoords(column_index, row_index))
                        else:
                            surface.blit(self.tileset.subsurface(self.tile_pixel_width * 2, 0, self.tile_pixel_width, self.tile_pixel_height), self.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(surface, self.static_map, row_index, column_index)
                    case 2:
                        surface.blit(self.tileset.subsurface(self.tile_pixel_width * 0, 0, self.tile_pixel_width, self.tile_pixel_height), self.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(surface, self.static_map, row_index, column_index)
                        self.checkpoint_tiles.append(pygame.Rect(*self.normalizeCoords(column_index, row_index, dynamic=True), self.tile_pixel_width, self.tile_pixel_height))
                    case 3:
                        surface.blit(self.tileset.subsurface(self.tile_pixel_width * 0, 0, self.tile_pixel_width, self.tile_pixel_height), self.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(surface, self.static_map, row_index, column_index)
                        self.spawn_tile = pygame.Rect(*self.normalizeCoords(column_index, row_index, dynamic=True), self.tile_pixel_width, self.tile_pixel_height)
                    case 4:
                        surface.blit(self.tileset.subsurface(self.tile_pixel_width * 0, 0, self.tile_pixel_width, self.tile_pixel_height), self.normalizeCoords(column_index, row_index))
                        self.drawLineIfThereIsWall(surface, self.static_map, row_index, column_index)
                        self.finish_tiles.append(pygame.Rect(*self.normalizeCoords(column_index, row_index, dynamic=True), self.tile_pixel_width, self.tile_pixel_height))
        return surface

    def normalizeCoords(self, x: int | float, y: int | float, dynamic: bool = False) -> tuple[int | float, int | float]:
        return (x * int(Map.config["Tilemap"]["tile_width"]) + dynamic * (int(Map.config["General"]["window_width"]) - self.map_pixel_width) // 2,
                y * int(Map.config["Tilemap"]["tile_height"]) + dynamic * (int(Map.config["General"]["window_height"]) - self.map_pixel_height) // 2)

    def drawLineIfThereIsWall(self, res: pygame.Surface, static_map: list, row_index: int, column_index: int):
        BLACK = [int(i) for i in Map.config["Colors"]["black"].split(", ")]
        if static_map[row_index - 1][column_index] == "0":  # Top
            pygame.draw.line(res, BLACK, self.normalizeCoords(column_index, row_index), self.normalizeCoords(column_index + 1, row_index), 3)
        if static_map[row_index][column_index - 1] == "0":  # Left
            pygame.draw.line(res, BLACK, self.normalizeCoords(column_index, row_index), self.normalizeCoords(column_index, row_index + 1), 3)
        if static_map[row_index + 1][column_index] == "0":  # Bottom
            pygame.draw.line(res, BLACK, self.normalizeCoords(column_index, row_index + 1), self.normalizeCoords(column_index + 1, row_index + 1), 3)
        if static_map[row_index][column_index + 1] == "0":  # Right
            pygame.draw.line(res, BLACK, self.normalizeCoords(column_index + 1, row_index), self.normalizeCoords(column_index + 1, row_index + 1), 3)
