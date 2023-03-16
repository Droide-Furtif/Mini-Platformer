import pygame
import sys
from player_class import Player
from walls import Wall, Spike
from laser_class import Laser
import UI
from collectibles import Collectible
from bumper_class import Bumper
from map_generator import Generator


class Game:

    def __init__(self):
        # Setup pygame
        pygame.init()
        self.screen = pygame.display.set_mode((900, 900))
        pygame.display.set_caption("Platformer")
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()

        # Setup variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.tick = 0
        self.show_hitboxes = False
        self.debug_mode = False

        # Setup Player
        self.player = Player(self)

        # Setup map
        self.wallList = []
        self.wallList.append(Wall(self, 0, 0, 2, 20))
        self.wallList.append(Wall(self, 2, 18, 7, 2))
        self.wallList.append(Wall(self, 12, 18, 8, 2))
        self.wallList.append(Wall(self, 6, 13, 4, 1))

        self.spikeList = []
        self.spikeList.append(Spike(self, 13, 17, 3, 1, 0))
        self.spikeList.append(Spike(self, 19, 15, 1, 3, 1))

        self.laserList = []
        self.laserList.append(Laser(self, 2, 13, 4, 1, 1))

        self.coinList = []
        self.coinList.append(Collectible(self, 8, 12))
        self.coinList.append(Collectible(self, 12, 14))

        self.bumperList = []

        # Setup UI
        self.ui = UI.UserInterface(self)

        # Setup Map-Generator
        #'''
        self.wallList = []
        self.spikeList = []
        self.laserList = []
        self.coinList = []


        self.generator = Generator(self)
        self.generator.loadMap('maps/map1.txt')
        #'''
        self.player.respawn()

        print("Initiated game")

    # GAME LOOP function
    def loop(self):
        while self.running:
            self.tick += 1
            self.checkEvents()
            self.player.update(self.tick)
            for laser in self.laserList:
                laser.update(self.tick)
            self.ui.update()
            self.draw()
            self.clock.tick(self.FPS)
        print("Game loop stopped running")

    # PYGAME EVENTS MANAGEMENT
    def checkEvents(self):
        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # KEYDOWN grab keys
            if event.type == pygame.KEYDOWN:
                # Get keys
                keys = pygame.key.get_pressed()
                # Soft close (Esc) or force close (ctrl+1)
                if keys[pygame.K_ESCAPE]:
                    self.running = False
                if keys[pygame.K_LCTRL] and keys[pygame.K_1]:
                    pygame.quit()
                    sys.exit()
                # Test key (U) and (I) - Show Hitboxes and Debug Mode
                if keys[pygame.K_u]:
                    self.show_hitboxes = not self.show_hitboxes if self.debug_mode else False
                if keys[pygame.K_i]:
                    self.debug_mode = not self.debug_mode
                    self.show_hitboxes = self.debug_mode
                # Player actions
                self.player.manageEvents(keys)

            # KEYUP grab keys
            if event.type == pygame.KEYUP:
                # Get keys
                keys = pygame.key.get_pressed()
                if not keys[pygame.K_d] and not keys[pygame.K_q]:
                    self.player.moveLeft = False
                    self.player.moveRight = False
                if not self.player.isDead:
                    if keys[pygame.K_d]:
                        self.player.moveRight = True
                        self.player.moveLeft = False
                    if keys[pygame.K_q]:
                        self.player.moveLeft = True
                        self.player.moveRight = False

    # SCREEN DISPLAY
    def draw(self):
        self.screen.fill('Black')
        for wall in self.wallList:
            wall.draw()
        for spike in self.spikeList:
            spike.draw()
        for laser in self.laserList:
            laser.draw()
        for coin in self.coinList:
            coin.draw()
        for bumper in self.bumperList:
            bumper.draw()

        self.player.draw()
        self.ui.draw()
        pygame.display.flip()
