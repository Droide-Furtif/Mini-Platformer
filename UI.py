import pygame


class UserInterface:
    def __init__(self, game):
        self.heart_sprite = pygame.image.load("images/heart.png").convert_alpha()
        self.heart_scaled = pygame.transform.scale(self.heart_sprite, (30,30))
        self.GAME = game
        self.win_size = (self.GAME.screenWidth, self.GAME.screenHeight)
        self.heart_pos = (self.win_size[0] *0.85 , self.win_size[1] *0.10)
        self.coin_pos = (self.win_size[0] *0.85 , self.win_size[1] *0.15)
        self.coin_text_pos = (self.coin_pos[0] +15, self.coin_pos[1] -8)
        self.hpCount = self.GAME.player.hp
        self.coinCount = self.GAME.player.coinCount

        pygame.font.init()
        self.kongfont_size = 14
        self.kongfont = pygame.font.Font("fonts/kongtext.ttf", self.kongfont_size)
        self.text_fps = self.kongfont.render("FPS: ", True, 'White')
        self.text_hitbox = self.kongfont.render("Hitboxes: ", True, 'White')
        self.text_coin = self.kongfont.render("", True, 'White')


    def update(self):
        self.hpCount = self.GAME.player.hp
        self.coinCount = self.GAME.player.coinCount

        self.text_fps = self.kongfont.render(f"FPS:{self.GAME.FPS}", True, 'White')
        self.text_hitbox = self.kongfont.render(f"Hitboxes: {self.GAME.show_hitboxes}", True, 'White')
        self.text_coin = self.kongfont.render(f"{self.coinCount}", True, 'White')

    def draw(self):
        # HP hearts drawing
        for i in range(self.hpCount):
            self.GAME.screen.blit(self.heart_scaled, (self.heart_pos[0] - i*32, self.heart_pos[1]))

        # Coin drawing
        pygame.draw.circle(self.GAME.screen, 'Yellow', self.coin_pos, 6)
        self.GAME.screen.blit(self.text_coin, self.coin_text_pos)

        # Debug mode
        if self.GAME.debug_mode:
            self.GAME.screen.blit(self.text_fps, (100,70))
            self.GAME.screen.blit(self.text_hitbox, (100, 90))
