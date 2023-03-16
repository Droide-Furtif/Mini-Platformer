import pygame

class Laser:
    def __init__(self, game, x=1, y=1, width=1, height=1, rot=0):
        self.GAME = game
        self.scale = 30
        self.gridX = x
        self.gridY = y
        self.pxlX = x * self.scale
        self.pxlY = y * self.scale
        self.width = width
        self.height = height
        self.rotation = rot
        self.rect = pygame.Rect(self.pxlX +12 - (2*rot), self.pxlY + 10 +(2*rot), self.width * self.scale-24 +(4*rot), self.height * self.scale -20 -(4*rot))
        self.sprite = pygame.image.load("images/laser.png").convert_alpha()

        self.active = True
        self.cooltime = 120

    def update(self, tick):
        if tick % self.cooltime == 0:
            self.active = not self.active

    def draw(self):
        self.GAME.screen.blit(pygame.transform.rotate(self.sprite, self.rotation*90), (self.pxlX, self.pxlY))
        self.GAME.screen.blit(pygame.transform.rotate(self.sprite, self.rotation*90 +180), (self.pxlX + (self.width-1) * self.scale, self.pxlY + (self.height-1)*self.scale))
        if self.active:
            pygame.draw.rect(self.GAME.screen, 'yellow3', self.rect)

    def collidesWithRect(self, argRect):
        return self.rect.colliderect(argRect) and self.active