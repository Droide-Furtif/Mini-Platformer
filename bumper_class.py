import pygame

class Bumper:
    def __init__(self, game, x, y):
        self.GAME = game
        self.scale = 30
        self.gridX = x
        self.gridY = y
        self.pxlX = x * self.scale
        self.pxlY = y * self.scale
        # 60*30px final sprite
        self.sprite = pygame.image.load('images/bumper.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.scale*2, self.scale))
        self.rect = pygame.Rect(self.pxlX + 8, self.pxlY+16, self.scale*2 - 16, self.scale -16)

        self.strength = 4

    def draw(self):
        self.GAME.screen.blit(self.sprite, (self.pxlX, self.pxlY))
        if self.GAME.show_hitboxes:
            pygame.draw.rect(self.GAME.screen, 'Red', self.rect, 2)


    def collidesWithRect(self, argRect):
        return self.rect.colliderect(argRect)