import pygame

class Collectible:
    def __init__(self, game, x, y):
        self.GAME = game
        self.x = x*30
        self.y = y*30

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        self.sprite = pygame.image.load("images/coin.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (20,20))

    def draw(self):
        self.GAME.screen.blit(self.sprite, (self.x, self.y))
        if self.GAME.show_hitboxes:
            pygame.draw.rect(self.GAME.screen, 'Red', self.rect, 2)

    def collidesWithRect(self, argRect):
        return self.rect.colliderect(argRect)