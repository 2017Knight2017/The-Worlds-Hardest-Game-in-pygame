from moving_objects import *
from map import Map
import pygame
from configparser import ConfigParser

pygame.init()
config = ConfigParser()
config.read("options.ini")
mainsurf = pygame.display.set_mode((640, 480))
pygame.display.set_caption("ddddd")
clock = pygame.time.Clock()
plr = Player()

while True:
    map_number = 1
    cur_map = Map(map_number)
    cur_map_surface, walls_tiles, spawn_tile, checkpoint_tile, finish_tiles = cur_map.generateSurface()
    plr.rect.center = spawn_tile.center
    while True:
        mainsurf.fill((216, 194, 255))
        mainsurf.blit(cur_map_surface, (0, 0))
        mainsurf.blit(plr.image, plr.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and plr.rect.x > 0:
            g = True
            for i in walls_tiles:
                if i.collidepoint(plr.rect.left - int(Player.config["Player"]["speed"]), plr.rect.centery):
                    g = False
                    break
            if g: plr.moveLeft()
        if keys[pygame.K_RIGHT] and plr.rect.x < (640 - plr.rect.width):
            g = True
            for i in walls_tiles:
                if i.collidepoint(plr.rect.right + int(Player.config["Player"]["speed"]), plr.rect.centery):
                    g = False
                    break
            if g: plr.moveRight()
        if keys[pygame.K_UP] and plr.rect.y > 0:
            g = True
            for i in walls_tiles:
                if i.collidepoint(plr.rect.centerx, plr.rect.top - int(Player.config["Player"]["speed"])):
                    g = False
                    break
            if g: plr.moveUp()
        if keys[pygame.K_DOWN] and plr.rect.y < (480 - plr.rect.height):
            g = True
            for i in walls_tiles:
                if i.collidepoint(plr.rect.centerx, plr.rect.bottom + int(Player.config["Player"]["speed"])):
                    g = False
                    break
            if g: plr.moveDown()

        """if exists(f"maps/MAP{'0' * (map_number < 10)}{map_number}-static.map") and exists(
                  f"maps/MAP{'0' * (map_number < 10)}{map_number}-dynamic.map"):
            map_number += 1
            break"""
        clock.tick(int(config["General"]["fps"]))
        pygame.display.update()
