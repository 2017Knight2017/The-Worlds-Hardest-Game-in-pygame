import pygame
from configparser import ConfigParser


class Topbar:
    config = ConfigParser()
    config.read("options.ini")

    def __init__(self):
        self.surface = pygame.Surface((int(Topbar.config["General"]["window_width"]), int(Topbar.config["Topbar"]["topbar_height"])))
        self.topbar_color = [int(i) for i in Topbar.config["Colors"]["topbar"].split(", ")]
        self.text_color = [int(i) for i in Topbar.config["Colors"]["text"].split(", ")]
        self.surface.fill(self.topbar_color)
        self.__font = pygame.font.SysFont("arial", 18, bold=True)

    def update(self, map_name, death_count):
        self.surface.blit(self.__font.render(map_name, 1, self.text_color, self.topbar_color), (5, 0))
        self.surface.blit(self.__font.render("MENU", 1, self.text_color, self.topbar_color), (280, 0))
        self.surface.blit(self.__font.render(f"Deaths: {death_count}", 1, self.text_color, self.topbar_color), (535, 0))

