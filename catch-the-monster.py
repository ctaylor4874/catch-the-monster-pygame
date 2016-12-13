import pygame
from random import randint
import math

KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275
#class to create a character
class Characters(object):
    def __init__(self, charImage, positionX, positionY, screen, width, height):
        self.width = width
        self.height = height
        self.charImage = charImage
        self.hero_x = positionX
        self.hero_y = positionY
        self.monster_x = randint(50, 440)
        self.monster_y = randint(50, 440)
        self.screen = screen
        self.goblin_x = randint(50, 440)
        self.goblin_y = randint(50, 440)
        self.goblin_direction = randint(0,3)
    #buffer to make sure monster does not spawn on hero
    def buffMonst(self, monster_x, monster_y):
        hero_x = 255
        hero_y = 240
        buffMonst = math.sqrt((hero_x - self.monster_x)**2 + (hero_y - self.monster_y)**2)
        while buffMonst < 200:
            self.monster_x = randint(50, 440)
            self.monster_y = randint(50, 440)
            buffMonst = math.sqrt((hero_x - self.monster_x)**2 + (hero_y - self.monster_y)**2)
    #buffer to make sure goblins do not spawn on hero
    def buffGob(self, goblin_x, goblin_y):
        hero_x = 255
        hero_y = 240
        buffGob = math.sqrt((hero_x - self.goblin_x)**2 + (hero_y - self.goblin_y)**2)
        while buffGob < 100:
            self.goblin_x = randint(50, 440)
            self.goblin_y = randint(50, 440)
            buffGob = math.sqrt((hero_x - self.goblin_x)**2 + (hero_y - self.goblin_y)**2)
    #update goblin direction
    def updateGoblin(self, change_dir_countdown):
        if change_dir_countdown == 0:
            self.goblin_direction = randint(0,3)
        if self.goblin_direction == 0:
            self.goblin_y-=.5
        if self.goblin_direction == 1:
            self.goblin_x+=.5
        if self.goblin_direction == 2:
            self.goblin_y+=.5
        if self.goblin_direction == 3:
            self.goblin_x-=.5

        self.screen.blit(self.charImage, (self.goblin_x, self.goblin_y))
        #enable goblins to pass through boundary to the other side of the game
        if self.goblin_x > self.width - 30:
            self.goblin_x = 30
        if self.goblin_x < 0:
            self.goblin_x = self.width -30
        if self.goblin_y > self.height - 30:
            self.goblin_y = 30
        if self.goblin_y < 0:
            self.goblin_y = self.height - 30
    #update monster direction
    def updateMonster(self, change_dir_countdown, direction):
        self.change_dir_countdown = change_dir_countdown
        self.direction = direction
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

        self.screen.blit(self.charImage, (self.monster_x, self.monster_y))
        #enable monster to pass through boundary to the other side of the game
        if self.monster_x > self.width - 30:
            self.monster_x = 30
        if self.monster_x < 0:
            self.monster_x = self.width -30
        if self.monster_y > self.height - 30:
            self.monster_y = 30
        if self.monster_y < 0:
            self.monster_y = self.height - 30
        #countdown to change monster direction
        self.change_dir_countdown-=1
        #return goblin direction and countdown number
        return self.change_dir_countdown, self.direction
    #make sure hero cannot pass through boudary and stops at boundary
    def updateHero(self):
        self.screen.blit(self.charImage, (self.hero_x, self.hero_y))

        if self.hero_x > self.width - 30:
            self.hero_x = self.width - 30
        if self.hero_x < 0:
            self.hero_x = 0
        if self.hero_y > self.height - 35:
            self.hero_y = self.height - 35
        if self.hero_y < 0:
            self.hero_y = 0

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
    goblin_image = pygame.image.load('images/goblin.png').convert_alpha()

    # set window caption
    pygame.display.set_caption('Catch The Monster')

    # create a clock
    clock = pygame.time.Clock()

    ################################
    # PUT INITIALIZATION CODE HERE #
    ################################
    change_dir_countdown = 0
    direction = 0
    goblin_direction = 0
    lost = False
    level = 1

    myHero = Characters(hero_image, 255, 140, screen, width, height)
    myGoblins = [
        Characters(goblin_image, 240, 100, screen, width, height)
        ]
    myMonster = Characters(monster_image, 240, 100, screen, width, height)
    stop_game = False
    #if round is won, increase level by 1
    def won_game(won, level):
        if won == True:
            level+=1
            return level
    loopSong = pygame.mixer.Sound('sounds/music.wav')
    # game loop
    while not stop_game:
        #start game song
        loopSong.play()
        #detect if hero collides with monster
        catch = math.sqrt((myHero.hero_x - myMonster.monster_x)**2 + (myHero.hero_y - myMonster.monster_y)**2)
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
        ################################
        # PUT CUSTOM DISPLAY CODE HERE #
        ################################
        if catch >= 25:
            screen.blit(background_image, (0, 0))
            lvl = pygame.font.SysFont("Comic Sans MS", 30)
            textsurfaceLevel = lvl.render("Level: %d" % (level), True, (255, 255, 255))
            screen.blit(textsurfaceLevel,(0,0))
            change_dir_countdown, direction = myMonster.updateMonster(change_dir_countdown, direction)
            myHero.updateHero()
            #update goblins from list myGoblins
            for n in range(len(myGoblins)):
                myGoblins[n].updateGoblin(change_dir_countdown)

        for i in range(len(myGoblins)):
            #detect if hero collides with goblin and set lost to True
            lose = math.sqrt((myHero.hero_x - myGoblins[i].goblin_x)**2 + (myHero.hero_y - myGoblins[i].goblin_y)**2)
            if lose < 25:
                lost = True
        if lost == True:
            #stop game music
            loopSong.stop()
            sound = pygame.mixer.Sound('sounds/lose.wav')
            screen.blit(background_image, (0, 0))
            #show goblins but hide hero and monster
            for i in range(len(myGoblins)):
                myGoblins[i].screen.blit(myGoblins[i].charImage, (myGoblins[i].goblin_x, myGoblins[i].goblin_y))
            lossText = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface = lossText.render('You lose! Would you like to play again?', False, (97, 159, 182))
            screen.blit(textsurface,(60,240))

            mySecond = pygame.font.SysFont("Comic Sans MS", 30)

            textsurface2 = mySecond.render('Press Enter for yes, or Q to exit the game.', False, (97, 159, 182))
            screen.blit(textsurface2,(60,260))
            #display level
            lvl = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface = lvl.render("Level: %d" % (level), False, (255, 255, 255))
            screen.blit(textsurface,(0,0))
            #play losing mosing
            sound.play()
            #listen for if enter is selected to play again
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        sound.stop()
                        screen.blit(background_image, (0, 0))
                        myHero.hero_x = 255
                        myHero.hero_y = 240
                        myMonster.monster_x = randint(40, 440)
                        myMonster.monster_y = randint(40, 440)
                        #make sure monster doesn't spawn on hero
                        myMonster.buffMonst(myMonster.monster_x, myMonster.monster_y)
                        myMonster.updateMonster(change_dir_countdown, direction)
                        #reset myGoblins to one item
                        myGoblins = [
                            Characters(goblin_image, 240, 100, screen, width, height)
                            ]
                        level = 1
                        #update goblin and make sure it doesn't spawn on hero
                        for goblin in myGoblins:
                            goblin.updateGoblin(change_dir_countdown)
                            goblin.buffGob(goblin.goblin_x, goblin.goblin_y)
                        myHero.updateHero()
                        lost = False
                    elif event.key == pygame.K_q:
                        stop_game = True
        #if hero catches monster before goblin catches him
        if catch < 25 and lost != True:
            #stop game music
            loopSong.stop()
            won = True
            catch = 25
            sound = pygame.mixer.Sound('sounds/win.wav')
            screen.blit(background_image, (0, 0))
            myFirst = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface = myFirst.render('You win! Would you like move on?', False, (97, 159, 182))
            screen.blit(textsurface,(60,240))

            mySecond = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface2 = mySecond.render('Press Enter for yes, or Q to exit the game.', False, (97, 159, 182))
            screen.blit(textsurface2,(60,260))
            #display hero but not goblins or monster
            myHero.screen.blit(myHero.charImage, (myHero.hero_x,
            myHero.hero_y))
            lvl = pygame.font.SysFont("Comic Sans MS", 30)
            textsurface = lvl.render("Level: %d" % (level), False, (255, 255, 255))
            screen.blit(textsurface,(0,0))
            #play victory music
            sound.play()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #listen if enter is selected to keep playing
                    if event.key == pygame.K_RETURN:
                        #add goblin to list of goblins
                        myGoblins.append(Characters(goblin_image, 240, 100, screen, width, height))
                        screen.blit(background_image, (0, 0))
                        #increase level
                        level = won_game(won, level)
                        #set won to false
                        won = False
                        myHero.hero_x = 255
                        myHero.hero_y = 240
                        #set monster at random point
                        myMonster.monster_x = randint(40, 440)
                        myMonster.monster_y = randint(40, 440)
                        #make sure monster doesn't spawn on hero
                        myMonster.buffMonst(myMonster.monster_x, myMonster.monster_y)
                        myMonster.updateMonster(change_dir_countdown, direction)
                        #update goblin position and make sure they dont spawn on hero
                        for goblin in myGoblins:
                            goblin.updateGoblin(change_dir_countdown)
                            goblin.buffGob(goblin.goblin_x, goblin.goblin_y)
                        buffMonst = math.sqrt((myHero.hero_x - myMonster.monster_x)**2 + (myHero.hero_y - myMonster.monster_y)**2)
                        while buffMonst < 70:
                            myMonster.monster_x = randint(40, 440)
                            myMonster.monster_y = randint(40, 440)
                            buffMonst = math.sqrt((myHero.hero_x - myMonster.monster_x)**2 + (myHero.hero_y - myMonster.monster_y)**2)
                        myHero.updateHero()
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
