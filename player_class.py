import pygame
import walls

class Player:

    def __init__(self, game):
        self.start_pos = (150, 700)
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.size = 38
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = "#80E280"
        self.GAME = game

        self.moveRight = False
        self.moveLeft = False
        self.isAirborne = True
        self.speed = 6
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
        self.canJump = True

        self.isDead = False
        self.deathCounter = 0
        self.baseHp = 1
        self.hp = self.baseHp
        self.immortal = False
        self.coinCount = 0

        self.death_circle_radius = 10
        self.death_circle_color = (255, 255, 255)

        self.temp_tick = 0

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
    def update(self, tick):
        # X movements
        self.x_velocity = 0
        self.x_velocity += int(self.moveRight)
        self.x_velocity -= int(self.moveLeft)
        self.x += self.speed * self.x_velocity
        self.rect.x = int(self.x)

        # Y movements
        if self.isAirborne:
            if self.y_velocity < self.max_y_vel:
                self.fallSpeed += self.fallSpeed / 10
                self.y_velocity += self.fallSpeed

        self.y += self.y_velocity
        self.rect.y = int(self.y)

        # Can jump or not
        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.canJump = True

        # Check collision with wall
        self.isLanded = False
        self.isAirborne = True
        self.isWalling = False
        for wall in self.GAME.wallList:
            # Landing collision
            if wall.collidesWithPoint((self.rect.midbottom[0] + self.size/4, self.rect.midbottom[1] -2)) \
        or wall.collidesWithPoint((self.rect.midbottom[0] - self.size/4, self.rect.midbottom[1] -2)):
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
                self.y_velocity = 1

            # Side collisions
            if wall.collidesWithPoint((self.rect.midleft[0]-1, self.rect.midleft[1])) \
                    or wall.collidesWithPoint((self.rect.midright[0]+1, self.rect.midright[1])):
                if wall.rect.left > self.rect.left:
                    self.x = wall.rect.left - self.size
                else:
                    self.x = wall.rect.right

                self.rect.x = self.x
                self.x_velocity = 0
                self.isWalling = True

        # Collision with Spikes
        for spike in self.GAME.spikeList:
            if spike.collidesWithRect(self.rect):
                self.takeDamage()

        # Collision with Lasers
        for laser in self.GAME.laserList:
            if laser.collidesWithRect(self.rect):
                self.takeDamage()

        # Collision with collectibles
        for coin in self.GAME.coinList:
            if coin.collidesWithRect(self.rect):
                self.addGold(1)
                self.GAME.coinList.remove(coin)
                del coin

        # Collision with bumpers
        for bumper in self.GAME.bumperList:
            if bumper.collidesWithRect(self.rect):
                self.hasJumped = False
                self.isLanded = True
                self.hasWallJumpedOnce = False
                self.hasWallJumpedTwice = False
                self.jump()
                self.y_velocity -= bumper.strength

        # Death trigger
        if self.hp <= 0 or self.rect.y > self.GAME.screenHeight:
            self.takeDamage()


    def jump(self):
        self.canJump = False
        if not self.hasJumped and self.isLanded:
            self.y -= 5
            self.hasJumped = True
            self.y_velocity = -self.jumpHeight
            #self.isWalling = False
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
                    print('walljump')

    def manageEvents(self, keys):
        # Keys Management
        if not self.isDead:
            if keys[pygame.K_d]:
                self.moveRight = True
            if keys[pygame.K_q]:
                self.moveLeft = True
            if keys[pygame.K_SPACE] and self.canJump:
                self.jump()

            if keys[pygame.K_d] and keys[pygame.K_q]:
                self.moveLeft = False
                self.moveRight = False
            if not keys[pygame.K_SPACE]:
                self.canJump = True

    # Respawn event
    def respawn(self):
        self.isDead = False
        self.deathCounter += 1
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
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
        self.moveLeft = self.moveRight = False

    def addGold(self, num: int):
        self.coinCount += num

    def setStartingPos(self, pos):
        self.start_pos = pos
