#memory version 3 

#The third version must acount for tiles matching. It starts with all the tiles hidden by displaying image0.bmp for each tile. When the player clicks on a tile, the tile becomes exposed until another tile is clicked. When two tiles are exposed the game will check if the images on those two exposed tiles are matching. if the two tiles are matching the tiles will remain exposed. if the two tiles are not matching they will return to their face down state. The game ends (the score should stop changing) when all 16 tiles are exposed.

from uagame import Window
import time
import pygame
from pygame.event import get as get_events
from random import shuffle
from pygame.locals import *
from pygame.time import Clock, get_ticks
from pygame.mouse import get_pos as pos

def main():

    window = Window('Memory', 500, 400)
    window.set_auto_update(False) #stop the constant redraw
    game = Game(window)
    game.play()
    window.close()

class Game:

    def __init__(self, window):
        self.pause_time = 0 
        self.window = window
        self.close_clicked = False
        self.continue_game = True
        self.load_images() 
        self.board = []
        self.board_size = 4
        Tile.set_window(window) #calling class method
        self.create_board()
        self.clock = Clock()
        self.score = 0
        self.compare_images = []
        self.match_count = 0
    
    def load_images(self):
    
        self.image_list = []
        for i in range(1,9):
            image = 'image' + str(i) + '.jpg'
            self.image_list.append(pygame.transform.scale(pygame.image.load(image), (100, 100)))
        self.image_list=self.image_list*2
        shuffle(self.image_list)
            
    
    
    def create_board(self):
        #for every row_index create a row
        for row_index in range(0, self.board_size):
            row = self.create_row(row_index)
            self.board.append(row)
    
    def create_row(self,row_index):
        row = []
        width = (self.window.get_width()-100)//4
        height = self.window.get_height()//4
        for col_index in range(0,self.board_size):
            image = self.image_list[row_index * 4 + col_index] 
            x = width * col_index 
            y = height * row_index 
            tile = Tile(x,y,width,height,image)
            row.append(tile)
        return row
    
    def play(self):
        while not self.close_clicked: 
            self.handle_events()
            #draw all the game objects
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time)
                        
        
    def handle_events(self):
        
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        
        elif event.type == MOUSEBUTTONUP:
            self.handle_mouse_up(event.pos)
            
    def handle_mouse_up(self,position): #position where the event happened
        for row in self.board:
            for tile in row: 
                if tile.select(position): #in Tile class
                    tile.show()
                    self.compare_images.append(tile)
            
    
    def update(self):
        #update the game score
        
        self.check_match()
        self.score = get_ticks() // 1000 
    
    def check_match(self):
        
        #if there is two images in the list, compare the two images. If they are the same, they remain face up, record tile_clicked as True, and the match count increments by one. If the two images are different, return the tiles to their face down state and record tile_clicked as False
        if len(self.compare_images) == 2:
            if self.compare_images[0] == self.compare_images[1]:
                self.match_count += 1
            else:
                time.sleep(1)
                self.compare_images[0].tile_down()
                self.compare_images[1].tile_down()
        
        
            self.compare_images = []
        
            
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        
        if self.match_count == 8:
            self.continue_game = False
            

    def draw(self):
        # Draw all game objects.
        # self is the Game to draw
        
        self.window.clear()
        #draw tiles
        for row in self.board:
            for tile in row:
                tile.draw()
        self.draw_score()
        self.window.update()
    
        
    def draw_score(self):
            self.window.set_font_size(60)
            string = '' + str(self.score)
            x = (self.window.get_width()) - self.window.get_string_width(str(self.score))
            y = 0
            self.window.draw_string(string, x, y)
            
            

class Tile:
    
    border_width = 4
    fg_color = 'black' 
    hidden_image = pygame.transform.scale(pygame.image.load('image0.jpg'), (100, 100))
    window = None #other class needs to access this class attribute, must create a class method.

    @classmethod
    def set_window(cls, window_from_Game):
        cls.window = window_from_Game
    
    #intance methods
    def __init__(self,x,y,width,height,image): #needed to create tile object
        
        self.image = image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,width,height)
        self.tile_clicked = False #check if tile has been clicked already
        
    def select(self, position):
        #sense whether or not this event is in the position or not
        if self.rect.collidepoint(position) and not self.tile_clicked:
            return True
        else:
            return False
        
    
    def draw(self):
        # draw the hidden tile if the tile is not clicked, draw the tile face up if it is clicked.
        surface = Tile.window.get_surface()
        if self.tile_clicked == False:
            surface.blit(Tile.hidden_image,(self.x,self.y))
            pygame.draw.rect(surface,pygame.Color(Tile.fg_color),self.rect,Tile.border_width)
        else:
            surface.blit(self.image,(self.x,self.y))
            pygame.draw.rect(surface,pygame.Color(Tile.fg_color),self.rect,Tile.border_width)
        
    def tile_down(self):
        self.tile_clicked = False
        
    def show(self):
        self.tile_clicked = True
            
    def __eq__(self,other_tile):
        #redefine the equality operator
        if self.image == other_tile.image:
            return True
        else:
            return False     
main()



