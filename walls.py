import pygame

class Wall:
    def __init__(self, game, x=1, y=1, width=1, height=1):
        self.GAME = game
        self.scale = self.GAME.screenWidth/30
        self.gridX = x
        self.pxlX = x * self.scale
        self.gridY = y
        self.pxlY = y * self.scale
        self.width = width * self.scale
        self.height = height * self.scale
        self.rect = pygame.Rect(self.pxlX, self.pxlY, self.width, self.height)
        self.color = 'White'

    def draw(self):
        pygame.draw.rect(self.GAME.screen, self.color, self.rect)

    def collidesWithRect(self, argRect):
        return self.rect.colliderect(argRect)

    def collidesWithPoint(self, point):
        return self.rect.collidepoint(point)


class Spike(Wall):
    def __init__(self, game, x=1, y=1, width=1, height=1, rot=0):
        super().__init__(game, x, y, width, height)
        self.sprite = pygame.image.load("images/spike.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (30,30))
        self.rect = pygame.Rect(self.pxlX, self.pxlY+10, self.width, self.height-10)
        self.rotation = rot
        self.sprite = pygame.transform.rotate(self.sprite, rot*90)

        # Do rotation for hitbox


    def draw(self):
        for i in range(int(self.width / self.scale)):
            for j in range(int(self.height / self.scale)):
                self.GAME.screen.blit(self.sprite, (self.pxlX + i*self.scale, self.pxlY + j*self.scale))

        if self.GAME.show_hitboxes:
            pygame.draw.rect(self.GAME.screen, 'RED', self.rect, 2)
