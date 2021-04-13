import pygame as pg
vec = pg.math.Vector2
import sys
import os
from random import choice, randrange

width = 500
height = 500  
gridsize = 4
tilesize = int(width / gridsize) 

class Game:
    def __init__(self):
        self.running = True
        pg.init()
        self.screen = pg.display.set_mode((width, height)) #initiates display
        self.clock = pg.time.Clock()
        self.images = [f for f in os.listdir() if f.endswith(('jpg', 'png'))] #gets list of every image in current directory
        pic = choice(self.images) #chooses random image from images
        img = pg.image.load(pic).convert() #loads image data
        self.tiles = pg.sprite.Group() #sprite group for tiles
        self.grid = Grid(self, img)
        
        self.time = 999 #finish time
        
    def run(self): #main loop
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        while not self.playing: #exit
            self.draw_text("you won! Press 'P' to play again", width // 2, height // 2)
            self.draw_text("your time: {} seconds".format(self.time), width // 2, height // 2 + 50)
            pg.display.flip()
            self.events()
            
    def events(self): #check for keyboard and mouse input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if pg.mouse.get_pressed()[0]: #if clicked on tile check to see if tile can be moved
                pos = vec(pg.mouse.get_pos())
                self.grid.move_tile(pos)
            if event.type == pg.KEYDOWN: #rescramble grid if p is pressed
                if event.key == pg.K_p:
                    self.grid.scramble()
                    self.playing = True
                        
    def update(self): #update display
        self.screen.fill((0, 0, 0, 0))
        self.win()
        
    def draw(self): #draw all tiles to screen
        for tile in self.grid.grid:
            if tile:
                self.screen.blit(tile.image, (int(tile.pos.x), int(tile.pos.y)))
        pg.display.flip()
        
    def win(self): #check for win condition
        if all(t.pos.x == t.winning_pos.x and t.pos.y == t.winning_pos.y for t in self.grid.grid if t):
        
            self.playing = False 
            
            self.time = str(pg.time.get_ticks() / 1000)
            
    def draw_text(self, text, x, y):
        font = pg.font.Font(pg.font.match_font('arial'), 30)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

class Tile(pg.sprite.Sprite):
    def __init__(self, img, game, x, y, color=(0, 0, 255)):
        pg.sprite.Sprite.__init__(self, game.tiles)
        self.pos = vec(x, y)
        self.image = pg.Surface((tilesize, tilesize))
        inside = pg.Surface((tilesize - 10, tilesize - 10))
        inside.blit(img, (0, 0), (x, y, tilesize - 10, tilesize - 10))
        self.rect = inside.get_rect()
        self.image.blit(inside,(5, 5))
        self.rect.x = int(self.pos.x + 5)
        self.rect.y = int(self.pos.y + 5)
        self.rangex = range(int(self.pos.x), int(self.pos.x + tilesize))
        self.rangey = range(int(self.pos.y), int(self.pos.y + tilesize))
        
        self.winning_pos = vec(x, y)
        
    def update_range(self):
        self.rangex = range(int(self.pos.x), int(self.pos.x + tilesize))
        self.rangey = range(int(self.pos.y), int(self.pos.y + tilesize))
        
class Grid:
    def __init__(self, game, img):
        self.game = game
        self.grid = [] #2d array for keeping track of where each tile is
        self.make_grid(img)
        self.rangex = range(0, width)
        self.rangey = range(0, height)
        self.scramble()
        
    def make_grid(self, img):
        for y in range(gridsize):
            for x in range(gridsize):
                if (y != gridsize - 1 or x != gridsize - 1):
                    self.grid.append(Tile(img, self.game, x * tilesize, y * tilesize))
                else:
                    self.grid.append(0)
               
    def move_tile(self, pos):
        for tile in self.grid:
            if tile:
                if pos[0] in tile.rangex and pos[1] in tile.rangey:
                    tile.rect.x += tilesize #right
                    hits = pg.sprite.spritecollide(tile, self.game.tiles, False)
                    tile.rect.x -= tilesize
                    if len(hits) == 1 and tile.rect.x + tilesize in self.rangex:
                        tile.pos.x += tilesize
                        tile.rect.x += tilesize
                        tile.update_range()
                        break
                    tile.rect.x -= tilesize #left
                    hits = pg.sprite.spritecollide(tile, self.game.tiles, False)
                    tile.rect.x += tilesize
                    if len(hits) == 1 and tile.rect.x - tilesize in self.rangex:
                        tile.pos.x -= tilesize
                        tile.rect.x -= tilesize
                        tile.update_range()
                        break
                    tile.rect.y += tilesize #down
                    hits = pg.sprite.spritecollide(tile, self.game.tiles, False)
                    tile.rect.y -= tilesize
                    if len(hits) == 1 and tile.rect.y + tilesize in self.rangey:
                        tile.pos.y += tilesize
                        tile.rect.y += tilesize
                        tile.update_range()
                        break
                    tile.rect.y -= tilesize #up
                    hits = pg.sprite.spritecollide(tile, self.game.tiles, False)
                    tile.rect.y += tilesize
                    if len(hits) == 1 and tile.rect.y - tilesize in self.rangey:
                        tile.pos.y -= tilesize
                        tile.rect.y -= tilesize
                        tile.update_range()
                        break
                        
    def scramble(self): #scrambles pieces, solution is always solvable
        for i in range(500 * (gridsize // 4)):
            pos = (randrange(tilesize // 2, width, tilesize), randrange(tilesize // 2, height, tilesize))
            self.move_tile(pos)
  
g = Game()
while g.running:
    g.run()
        
        
    

