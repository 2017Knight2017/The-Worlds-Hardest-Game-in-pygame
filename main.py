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
map_number = 0

while True:
    cur_map = Map(map_number)
    cur_map_surface = cur_map.generateSurface()
    plr = Player(cur_map.spawn_tile.center)
    coins = pygame.sprite.Group()
    for i in cur_map.coins_coords:
        coins.add(Coin(i))
    while True:
        mainsurf.fill(list(map(int, config["Colors"]["background"].split(", "))))
        mainsurf.blit(cur_map_surface, (0, 0))
        mainsurf.blit(plr.image, plr.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and plr.rect.x > 0:
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.rect.left - float(Player.config["Player"]["speed"]), plr.rect.centery):
                    g = False
                    break
            if g: plr.moveLeft()
        if keys[pygame.K_RIGHT] and plr.rect.x < (640 - plr.rect.width):
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.rect.right + float(Player.config["Player"]["speed"]), plr.rect.centery):
                    g = False
                    break
            if g: plr.moveRight()
        if keys[pygame.K_UP] and plr.rect.y > 0:
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.rect.centerx, plr.rect.top - float(Player.config["Player"]["speed"])):
                    g = False
                    break
            if g: plr.moveUp()
        if keys[pygame.K_DOWN] and plr.rect.y < (480 - plr.rect.height):
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.rect.centerx, plr.rect.bottom + float(Player.config["Player"]["speed"])):
                    g = False
                    break
            if g: plr.moveDown()

        pygame.sprite.spritecollide(plr, coins, True)
        if plr.next_level:
            map_number += 1
            break

        coins.draw(mainsurf)
        plr.update(cur_map.checkpoint_tiles, cur_map.finish_tiles, coins)
        clock.tick(int(config["General"]["fps"]))
        pygame.display.update()
