from pygame.locals import *
from random import randint
import pygame
import time
import json
import pygame_textinput
import pandas as pd

pygame.init()

#set standards for start screen 
"using vectors may be better than x,y coordinate plane, look up how to"
"create vectors for this."

white = (255,255,255)
green = (0, 160, 0)
black = (0,0,0)
smallfont = pygame.font.SysFont("arial", 25)
medfont = pygame.font.SysFont("arial", 50)
largefont = pygame.font.SysFont("arial", 80)
display_height = 600
display_width = 800
gameDisplay = pygame.display.set_mode((800,600))
background = pygame.image.load("start_menu.png")

def saved_high_score():
    with open('snake_name_highscore.json') as snake:
        json.load(snake) 
        
    
def start_screen():
    
    intro = True
    
    while intro:
    
        gameDisplay.blit(background,(0,0))

        message_to_screen(gameDisplay,"Tyce's Snake Game", green,0, -100, size ="large")
        message_to_screen(gameDisplay,"Eat the Mouse with the Snake", black,0, 45, size="small")
        message_to_screen(gameDisplay,"Each mouse is 10 points", black,0, 70, size="small")
        message_to_screen(gameDisplay,"If the Snake eats itself GAME OVER", black,0, 95, size="small")
        message_to_screen(gameDisplay,"Press SPACEBAR to play and Q to QUIT", black,0, 120, size="small")
        message_to_screen(gameDisplay,"Use arrow keys to move snake", black,0, 145, size="small")
        
        
        pygame.display.update()

        #start and stop for the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
def message_to_screen(screen, msg,color,x_displace=0, y_displace=0, size = "small",):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2)+x_displace, (display_height / 2)+y_displace
    screen.blit(textSurf, textRect)
    # display the screen with text and image
    
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    
    
    return textSurface, textSurface.get_rect()

    
    

    
class Mouse:
    x = 0
    y = 0
    step = 44
    
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
    
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*44
       self.x[2] = 2*44
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0

    
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
 
class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
    mouse = 0
    

       
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._mouse_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.mouse = Mouse(5,5)
        self.score = 0
        self.collision = False
        self.saved = False
        
    def on_init(self):
        pygame.init() 
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        #print(self._display_surf)
        pygame.display.set_caption('Tyce Snake Game')
        self._running = True
        self._image_surf = pygame.image.load("snake.png").convert()
        self._mouse_surf = pygame.image.load("mouse.png").convert()
        
        
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        #print("on_loop")
        self.player.update()
        
        
        # does snake eat mouse?
        for i in range(0,self.player.length):
            
            if self.game.isCollision(self.mouse.x,self.mouse.y,self.player.x[i], self.player.y[i],44):
                self.mouse.x = randint(2,9) * 44
                self.mouse.y = randint(2,9) * 44
                self.player.length = self.player.length + 1
                self.score += 10
                   
                #self._display_surf.blit(self.score,white, 150, size='small')
                #self.message_to_screen(str(self.score), white, 30, size = "large")
 
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                self.collision = True

    def on_render(self):
        
        if self.collision == False:
            self._display_surf.fill((0,0,0))
            self.player.draw(self._display_surf, self._image_surf)
            self.mouse.draw(self._display_surf, self._mouse_surf)
            message_to_screen(self._display_surf, "Score = "+str(self.score), white,330, -280, size = "small")

        else:
            self.final_screen()

        if self.saved == True:
            self.final_screen()

        
        pygame.display.flip()

    def final_screen(self):
        
        keys = pygame.key.get_pressed() 
 
        final_screen_window = pygame.display.set_mode((800,600))
        message_to_screen(final_screen_window,"Game Over!",white,0,-100,size="large")
        message_to_screen(final_screen_window,"Final Score: "+str(self.score),white,0,-20,size="large")
        message_to_screen(final_screen_window,"Press w to save name and score",white,0,40,size="medium")
        message_to_screen(final_screen_window,"Press m for start screen",white,0,80,size="medium")
        message_to_screen(final_screen_window,"Press p to play again",white,0,130,size="medium")
        message_to_screen(final_screen_window,"",white,-50,90,size="small")
        
        if (keys[K_w]):
            self.initials()
        
        if (keys[K_m]):
            start_screen()

        if (keys[K_p]):
            theApp = App()
            theApp.on_execute()
            
    def initials(self):
        saved_name =[]
        textinput = pygame_textinput.TextInput()
        keys = pygame.key.get_pressed()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        name_been_saved = False
        initials_type = True
        
        while initials_type == True:
            screen.fill((225, 225, 225))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Feed it with events every frame
            textinput.update(events)
            # Blit its surface onto the screen
            screen.blit(textinput.get_surface(), (10, 10))
    
            pygame.display.update()
            clock.tick(30)
            if textinput.update(events):
                print(textinput.get_text())
                score_save = (repr(self.score))
                name_save = (str(textinput.get_text()) ,score_save)
                saved_name.append(name_save)
                
                with open('snake_name_highscore.json', 'w') as snake:
                    json.dump(saved_name, snake)
                    print("Saved!")
                    initials_type = False
                    
        if initials_type == False:
            self.final_screen()
 
    def on_cleanup(self):
        #quit game
        pygame.quit()
        
        #displey score and prompt user input of name
        #save to json file
        #load game agian on correct prompt
        
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    start_screen()
    theApp = App()
    theApp.on_execute()
