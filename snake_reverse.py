#reverse snake game
from winsound import PlaySound
import pygame
from pygame.locals import *         # imports certain global Variables
import time




SIZE = 16
Start = 100

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 10 
        self.y = SIZE * 5
        self.counter = 20                   #counter to count loops till movement
        self.current = 20                  #current loops since last movement
        self.direc = "down"
    
    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):   #from normal snake
        self.direc = 'left'

    def move_right(self):
        self.direc = 'right'

    def move_up(self):
        self.direc = 'up'

    def move_down(self):
        self.direc = 'down'

    def move(self):             #movement taken from snake head
        if self.direc == 'left':
            self.x -= SIZE
        if self.direc == 'right':
            self.x += SIZE
        if self.direc == 'up':
            self.y -= SIZE
        if self.direc == 'down':
            self.y += SIZE 
            
    



class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.head = pygame.image.load("resources/greeneye.jpeg").convert()     #importing a picture
        self.block = pygame.image.load("resources/green.jpeg").convert()

        self.length = length
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.counter = 20                  #counter to count loops till movement
        self.current = 20                  #current loops since last movement
        self.length_increase_counter = 0
       
        for i in range (self.length):
            self.x.append(Start )
            self.y.append(Start + SIZE*i)

        self.direc = 'down'

    def set_direction(self, xa, ya, xb, yb):
        x = xa - xb
        y = ya - yb
        if abs(x) > abs(y):
            if x > 0:
                self.direc = "right"
            else:
                self.direc = "left"
        else:
            if y > 0:
                self.direc = "down"
            else:
                self.direc = "up"


        
    def move(self):
        #update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direc == 'left':
            self.x[0] -= SIZE
        if self.direc == 'right':
            self.x[0] += SIZE
        if self.direc == 'up':
            self.y[0] -= SIZE
        if self.direc == 'down':
            self.y[0] += SIZE



    def draw(self):
        self.parent_screen.blit(self.head, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))                         #drawing the image        ((0,0) is upper left corner) 
        pygame.display.flip()                                       #update screen

    
    def length_increase(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

        
class Game:
    def __init__(self):
        pygame.init()               #initialising the pygame module
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        pygame.mixer.init()                     #initzializing sound module

        self.play_background_music()
        
        self.surface = pygame.display.set_mode((SIZE * 30, SIZE * 25))             #initialising the window and its properties, size in pixels
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.game_over_type = 0          # = 1 if won, = 2 if lost
        

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-3}", True, (255, 255, 255))
        self.surface.blit(score, (320, 20))
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE: 
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',20)
        if self.game_over_type == 1:
            line1 = font.render(f"You won. Congratulations. Your score: {self.snake.length-3}", True, (255, 255, 255))
            self.surface.blit(line1, (50, 100))
            line2 = font.render(f"To play again press Enter. To exit press Escape", True, (255, 255, 255))
            self.surface.blit(line2, (50, 150))
        elif self.game_over_type == 2:
            line1 = font.render(f"The game is over. Your score: {self.snake.length-3}", True, (255, 255, 255))
            self.surface.blit(line1, (50, 100))
            line2 = font.render(f"To play again press Enter. To exit press Escape", True, (255, 255, 255))
            self.surface.blit(line2, (50, 150))
        else:
            line1 = font.render("Unexpected Error occurred", True, (255, 255, 255))
            self.surface.blit(line1, (50, 100))
            line2 = font.render("To play again press Enter. To exit press Escape", True, (255, 255, 255))
            self.surface.blit(line2, (50, 150))


        pygame.display.flip()

        pygame.mixer.music.pause()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
        pygame.mixer.Sound.set_volume(sound, 0.2)
    
    def play_background_music(self):
        pygame.mixer.music.load("resources/bensound-happyrock.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

    def render_background(self):
        bg = pygame.image.load("resources/background_green.jpeg")
        self.surface.blit(bg, (0, 0))

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
    

    def play(self):
        if self.snake.current >= self.snake.counter:
            if self.snake.length_increase_counter >= 50:
                self.snake.length_increase()
                if self.snake.counter > 14:
                    self.snake.counter -= 1
                self.snake.length_increase_counter = 0

            self.snake.current = 0
            self.snake.set_direction(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0])
            self.snake.move()
            self.snake.current = 0
            

        if self.apple.current >= self.apple.counter:
            self.apple.current = 0
            self.apple.move()

        if self.is_collision(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0]):
            self.game_over_type = 2
            raise "Game over"

        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.game_over_type = 1
                raise "Game over"
        
        



        self.render_background()
        self.apple.draw()
        self.snake.draw()
        

        self.snake.current += 1
        self.apple.current += 1
        self.snake.length_increase_counter += 1

    def run(self):
        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    
                    if not False:
                        if event.key == K_LEFT:
                            self.apple.move_left()
                        if event.key == K_RIGHT:
                            self.apple.move_right()
                        if event.key == K_UP:
                            self.apple.move_up()
                        if event.key == K_DOWN:
                            self.apple.move_down()

                elif event.type == QUIT:
                    running = False
            #self.play()
            try:
                if not pause:
                    self.play()
            except Exception as e: 
                self.show_game_over()
                pause = True
                self.reset()


            time.sleep(0.01)

        

if __name__ == "__main__":
    game = Game()
    game.run()