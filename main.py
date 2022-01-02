from moving_objects import *
from map import Map
import pygame

pygame.init()
mainsurf = pygame.display.set_mode((640, 480))
pygame.display.set_caption("ddddd")
clock = pygame.time.Clock()
plr = Player()

while True:
    map_number = 1
    cur_map = Map(map_number)
    cur_map_surface, spawn, checkpoints, finish_tiles = cur_map.generateSurface()
    plr.rect.center = spawn.center
    while True:
        mainsurf.fill((216, 194, 255))
        mainsurf.blit(cur_map_surface, (0, 0))
        mainsurf.blit(plr.image, plr.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and plr.rect.x > 0:
            plr.moveLeft()
        if keys[pygame.K_RIGHT] and plr.rect.x < (640 - plr.rect.width):
            plr.moveRight()
        if keys[pygame.K_UP] and plr.rect.y > 0:
            plr.moveUp()
        if keys[pygame.K_DOWN] and plr.rect.y < (480 - plr.rect.height):
            plr.moveDown()

        """if exists(f"maps/MAP{'0' * (map_number < 10)}{map_number}-static.map") and exists(
                  f"maps/MAP{'0' * (map_number < 10)}{map_number}-dynamic.map"):
            map_number += 1
            break"""
        clock.tick(60)
        pygame.display.update()
