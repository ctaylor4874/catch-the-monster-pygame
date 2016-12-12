import pygame
from random import randint
import math

KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275

class Characters(object):
    def __init__(self, hero_x, hero_y, screen, images):
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.characterPos = randint(36, 200)
        self.characterPos = randint(36, 200)

class Hero(object):
    def __init__(self, hero_x, hero_y, screen, hero_image):
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.screen = screen
        self.hero_image = hero_image

    def update(self, width, height):
        self.screen.blit(self.hero_image, (self.hero_x, self.hero_y))

        if self.hero_x > width - 30:
            self.hero_x = width - 30
        if self.hero_x < 0:
            self.hero_x = 0
        if self.hero_y > height - 35:
            self.hero_y = height - 35
        if self.hero_y < 0:
            self.hero_y = 0

class Monster(object):
    def __init__(self, monster_x, monster_y, screen, monster_image, direction):
        self.monster_x = monster_x
        self.monster_y = monster_y
        self.screen = screen
        self.monster_image = monster_image
        self.change_dir_countdown = 0
        self.direction = direction

    def update(self, width, height):
        if self.change_dir_countdown == 0:
            self.change_dir_countdown = 120
            self.direction = randint(0,3)

        if self.direction == 0:
            self.monster_y-=1
        if self.direction == 1:
            self.monster_x+=1
        if self.direction == 2:
            self.monster_y+=1
        if self.direction == 3:
            self.monster_x-=1

        self.screen.blit(self.monster_image, (self.monster_x, self.monster_y))

        if self.monster_x > width - 30:
            self.monster_x = 30
        if self.monster_x < 0:
            self.monster_x = width -30
        if self.monster_y > height - 30:
            self.monster_y = 30
        if self.monster_y < 0:
            self.monster_y = height - 30

        self.change_dir_countdown-=1

def main():
    # declare the size of the canvas
    width = 510
    height = 480

    # initialize the pygame framework
    pygame.init()
    pygame.font.init()
    # create screen
    screen = pygame.display.set_mode((width, height))

    background_image = pygame.image.load('images/background.png').convert_alpha()
    hero_image = pygame.image.load('images/hero.png').convert_alpha()
    monster_image = pygame.image.load('images/monster.png').convert_alpha()

    # set window caption
    pygame.display.set_caption('Catch The Monster')

    # create a clock
    clock = pygame.time.Clock()

    ################################
    # PUT INITIALIZATION CODE HERE #
    ################################
    myHero = Hero(255, 240, screen, hero_image)
    myMonster = Monster(240, 100, screen, monster_image, 0)
    # game loop
    stop_game = False
    while not stop_game:
        catch = math.sqrt((myHero.hero_x - myMonster.characterPos)**2 + (myHero.hero_y - myMonster.monster_y)**2)
        # look through user events fired
        if catch >= 25:
            for event in pygame.event.get():
                ################################
                # PUT EVENT HANDLING CODE HERE #
                ################################
                if event.type == pygame.KEYDOWN:
                    if event.key == KEY_DOWN:
                        myHero.hero_y += 20
                    elif event.key == KEY_UP:
                        myHero.hero_y -= 20
                    elif event.key == KEY_LEFT:
                        myHero.hero_x -= 20
                    elif event.key == KEY_RIGHT:
                        myHero.hero_x += 20

                if event.type == pygame.QUIT:
                    # if they closed the window, set stop_game to True
                    # to exit the main loop
                    stop_game = True
        #######################################
        # PUT LOGIC TO UPDATE GAME STATE HERE #
        #######################################

        if catch > 25:
            screen.blit(background_image, (0, 0))

            myMonster.update(width, height)
            myHero.update(width, height)


        ################################
        # PUT CUSTOM DISPLAY CODE HERE #
        ################################
        if catch <= 25:
            screen.blit(background_image, (0, 0))
            myFirst = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface = myFirst.render('You win! Would you like to play again?', False, (97, 159, 182))
            screen.blit(textsurface,(60,240))

            mySecond = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface2 = mySecond.render('Press Enter for yes, or Q to exit the game.', False, (97, 159, 182))
            screen.blit(textsurface2,(60,260))

            myHero.screen.blit(myHero.hero_image, (myHero.hero_x, myHero.hero_y))
            sound = pygame.mixer.Sound('win.wav')
            sound.play()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        screen.blit(background_image, (0, 0))
                        myHero.hero_x = 255
                        myHero.hero_y = 240
                        myMonster.characterPos = 240
                        myMonster.monster_y = 100
                        myMonster.update(width, height)
                        myHero.update(width, height)
                    elif event.key == pygame.K_q:
                        stop_game = True

        # update the canvas display with the currently drawn frame
        pygame.display.update()

        # tick the clock to enforce a max framerate
        clock.tick(60)

    # quit pygame properly to clean up resources
    pygame.quit()

if __name__ == '__main__':
    main()
