import pygame
import numpy
import walls

class Player:

    def __init__(self, game):
        self.x = 200
        self.y = 200
        self.size = 30
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = "#80E280"
        self.GAME = game

        self.isMoving = [0, 0]  # 0,0 STILL | 1,0 RIGHT | -1,-1 UP LEFT
        self.isAirborne = True
        self.speed = 4
        self.baseFallSpeed = 0.05
        self.fallSpeed = self.baseFallSpeed
        self.x_velocity = 0
        self.y_velocity = 0
        self.max_y_vel = 10
        self.jumpHeight = 7
        self.hasJumped = True
        self.isLanded = False
        self.isWalling = False
        self.hasWallJumpedOnce = False
        self.hasWallJumpedTwice = False

        self.isDead = False
        self.baseHp = 1
        self.hp = self.baseHp
        self.immortal = False
        self.coinCount = 0

        self.death_circle_radius = 10
        self.death_circle_color = (255, 255, 255)

    # Draw on screen
    def draw(self):
        pygame.draw.rect(self.GAME.screen, self.color, self.rect)

        # Death anim
        if self.isDead:
            pygame.draw.circle(self.GAME.screen, self.death_circle_color, self.rect.center, self.death_circle_radius, 3)
            pygame.draw.circle(self.GAME.screen, self.death_circle_color, self.rect.center, self.death_circle_radius + 4, 1)
            pygame.draw.circle(self.GAME.screen, self.death_circle_color, self.rect.center, self.death_circle_radius - 5, 2)
            self.death_circle_radius += 1.5
            _ = self.death_circle_radius * 3
            self.death_circle_color = (255 - _, 255 - _, 255 - _)
            # Reset and respawn when anim ends
            if self.death_circle_radius > 85:
                self.death_circle_radius = 10
                self.death_circle_color = (255, 255, 255)
                self.respawn()
                self.immortal = False
                print("resp")

    # Update (loop)
    def update(self):
        # X movements
        self.x += self.speed * numpy.sign(self.isMoving[0])
        self.rect.x = int(self.x)

        # Y movements
        if self.isAirborne:
            if self.y_velocity < self.max_y_vel:
                self.fallSpeed += self.fallSpeed / 10
                self.y_velocity += self.fallSpeed

        self.y += self.y_velocity
        self.rect.y = int(self.y)

        # Check collision with wall
        self.isLanded = False
        self.isAirborne = True
        self.isWalling = False
        for wall in self.GAME.wallList:
            # Landing collision
            if wall.collidesWithPoint((self.rect.midbottom[0], self.rect.midbottom[1] -2)):
                self.rect.bottom = wall.rect.top
                self.isAirborne = False
                self.fallSpeed = self.baseFallSpeed
                self.hasJumped = False
                self.hasWallJumpedOnce = self.hasWallJumpedTwice = False
                self.isLanded = True
                self.y_velocity = 0
                self.x = self.rect.x

            # Top collision
            if wall.collidesWithPoint(self.rect.midtop):
                self.y_velocity = 0

            # Side collisions
            if wall.collidesWithPoint((self.rect.midleft[0]-1, self.rect.midleft[1])) \
                    or wall.collidesWithPoint((self.rect.midright[0]+1, self.rect.midright[1])):
                if wall.rect.left > self.rect.left:
                    self.x = wall.rect.left - self.size
                else:
                    self.x = wall.rect.right

                self.rect.x = self.x
                self.isMoving[0] = 0
                self.isWalling = True
                print("wall")

        # Collision with Spikes
        for spike in self.GAME.spikeList:
            if spike.collidesWithRect(self.rect):
                self.takeDamage()

        # Collision with collectibles
        for coin in self.GAME.coinList:
            if coin.collidesWithRect(self.rect):
                self.addGold(1)
                self.GAME.coinList.remove(coin)
                del coin

        # Death trigger
        if self.hp <= 0 or self.rect.y > self.GAME.screenHeight:
            self.takeDamage()


    def jump(self):
        if not self.hasJumped and self.isLanded:
            self.y -= 3
            self.hasJumped = True
            self.y_velocity = -self.jumpHeight
            self.isWalling = False
            self.fallSpeed = self.baseFallSpeed
            self.isAirborne = True
            print("jump")
        else:
            if self.isWalling:
                if not self.hasWallJumpedTwice:
                    self.y_velocity = -self.jumpHeight
                    self.isWalling = False
                    self.fallSpeed = self.baseFallSpeed
                    if self.hasWallJumpedOnce:
                        self.hasWallJumpedTwice = True
                    else:
                        self.hasWallJumpedOnce = True

    def manageEvents(self, keys):
        # Keys Management
        if not self.isDead:
            if keys[pygame.K_d]:
                self.isMoving[0] = 1
            if keys[pygame.K_q]:
                self.isMoving[0] = -1
            if keys[pygame.K_SPACE]:
                self.jump()

            if keys[pygame.K_d] and keys[pygame.K_q]:
                self.isMoving[0] = 0

    # Respawn event
    def respawn(self):
        self.isDead = False
        self.x = 200
        self.y = 200
        self.rect.x = self.x
        self.rect.y = self.y
        if self.hp <= 0:
            self.hp = self.baseHp

    def takeDamage(self):
        if not self.immortal:
            self.hp -= 1
            if self.hp <= 0:
                self.death()
                self.immortal = True
            else:
                self.respawn()

    # Death event
    def death(self):
        self.isDead = True
        self.isMoving[0] = self.isMoving[1] = 0

    def addGold(self, num: int ):
        self.coinCount += num
