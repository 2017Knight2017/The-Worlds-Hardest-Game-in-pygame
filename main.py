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
plr = pygame.sprite.GroupSingle()

while True:
    cur_map = Map(map_number)
    cur_map_surface = cur_map.generateSurface()
    plr.add(Player(cur_map.spawn_tile.center if plr.sprite is None or plr.sprite.respawn_pos is None or plr.sprite.next_level else plr.sprite.respawn_pos))
    coins = pygame.sprite.Group([Coin(i) for i in cur_map.coins_coords])
    enemies = pygame.sprite.Group()
    for i in cur_map.enemies_data:
        match i["movement_type"]:
            case "from_to":
                enemies.add([Enemy(i["init_pos"], i["movement_type"], i["color"], i["speed"], key_positions=i["key_positions"])])
            case "around":
                enemies.add([Enemy(i["init_pos"], i["movement_type"], i["color"], i["speed"], circle_center=i["circle_center"])])
    while True:
        mainsurf.fill(list(map(int, config["Colors"]["background"].split(", "))))
        mainsurf.blit(cur_map_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.sprite.rect.left - float(Player.config["Player"]["speed"]), plr.sprite.rect.centery):
                    g = False
                    break
            if g: plr.sprite.moveLeft()
        if keys[pygame.K_RIGHT]:
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.sprite.rect.right + float(Player.config["Player"]["speed"]), plr.sprite.rect.centery):
                    g = False
                    break
            if g: plr.sprite.moveRight()
        if keys[pygame.K_UP]:
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.sprite.rect.centerx, plr.sprite.rect.top - float(Player.config["Player"]["speed"])):
                    g = False
                    break
            if g: plr.sprite.moveUp()
        if keys[pygame.K_DOWN]:
            g = True
            for i in cur_map.walls_tiles:
                if i.collidepoint(plr.sprite.rect.centerx, plr.sprite.rect.bottom + float(Player.config["Player"]["speed"])):
                    g = False
                    break
            if g: plr.sprite.moveDown()

        pygame.sprite.spritecollide(plr.sprite, coins, True)
        if pygame.sprite.spritecollide(plr.sprite, enemies, False):
            break

        if plr.sprite.next_level:
            map_number += 1
            break

        enemies.update()
        plr.update(cur_map.checkpoint_tiles, cur_map.finish_tiles, coins)
        enemies.draw(mainsurf)
        coins.draw(mainsurf)
        plr.draw(mainsurf)
        clock.tick(int(config["General"]["fps"]))
        pygame.display.update()
