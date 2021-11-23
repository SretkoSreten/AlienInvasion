import pygame 
import os
import random

pygame.init()

pygame.font.init()

WIDTH, HEIGHT = 350, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invesion")
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BACKGROUND_IMAGE = pygame.image.load('*/images/background-black.png')
BACKGROUND_SCREEN = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

sprite_sheet = SpriteSheet('C:/Users/PC/Desktop/Python/games/alien invesion/images/sprites.png') 


class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = 38
        self.height = 43
        self.pos_x = 160
        self.pos_y = 0
        self.bullets = []
        self.dx = 1
        self.dy = 1
        self.image = image
        self.enemy = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_time = pygame.time.get_ticks()
        self.shot_cooldown = 200
        self.vel_x = 2
        self.vel_y = 1

    def draw(self):
        WIN.blit(self.enemy, (self.x - self.width / 2,
        self.y - self.height / 2))

    def update(self):

        self.x += (self.vel_x * self.dx)
        self.y += self.vel_y

        if self.x - self.width / 2 < 0:
            self.dx = -self.dx
        if self.x + self.width / 2 > WIDTH:
            self.dx = -self.dx

    def collison(self, bullet, bullet1):
        if bullet.y < self.y + self.height / 2 and bullet.x > self.x and bullet.x < self.x + self.width:
            return True
        if bullet1.y < self.y + self.height / 2 and bullet1.x > self.x and bullet1.x < self.x + self.width:
            return True

        return False

    def shot(self):
        bullet = Bullet(self.x, self.y, self.dy)
        if pygame.time.get_ticks() - self.update_time > self.shot_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.bullets.append(bullet)

class Bullet:
    def __init__(self, x, y, dy):
        self.x = x
        self.y = y
        self.pos_x = 0
        self.pos_y = 45
        self.dy = dy
        self.width = 3
        self.height = 20
        self.speed = 5
        self.image = sprite_sheet.get_sprite(self.pos_x, self.pos_y, self.width, self.height)
        self.rect = self.image.get_rect()

    def draw(self):

        WIN.blit(self.image, (self.x - self.width / 2,
        self.y - self.height / 2))

    def update(self):
        self.y += (self.speed * self.dy)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.width = 38
        self.height = 43
        self.isAlive = True
        self.dy = -1
        self.image = sprite_sheet.get_sprite(0, 0, self.width, self.height)
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.update_time = pygame.time.get_ticks()
        self.shot_cooldown = 200

    def draw(self):
        WIN.blit(self.image, (self.x - self.width / 2,
        self.y - self.height / 2))

    def movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed
        if keys_pressed[pygame.K_SPACE]:
            self.shot()

    def update(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2
        if self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2
    
    def collison(self, bullet):
        if bullet.y >= self.y and bullet.x > self.x - self.width and bullet.x < self.x + self.width and bullet.y <= self.y + self.height:
            return True
        return False

    def shot(self):

        bullet1 = Bullet(self.x - self.width / 3, self.y, self.dy)
        bullet2 = Bullet(self.x + self.width / 3, self.y, self.dy)

        if pygame.time.get_ticks() - self.update_time > self.shot_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.bullets.append([bullet1, bullet2])

def draw_window():
    WIN.blit(BACKGROUND_SCREEN, (0, 0))

def draw_win():
    font = pygame.font.SysFont(None, 50)
    img = font.render(f"Winner !!", True, WHITE)
    WIN.blit(img, (int(WIDTH / 2 - img.get_width() / 2), 
    int(HEIGHT / 2 - img.get_height() / 2)))

def draw_score(score):
    font = pygame.font.SysFont(None, 30)
    img = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(img, (20, 20))

def game_over():
    font = pygame.font.SysFont(None, 50)
    img = font.render(f"GAME OVER !!", True, WHITE)
    WIN.blit(img, (int(WIDTH / 2 - img.get_width() / 2), 
    int(HEIGHT / 2 - img.get_height() / 2)))


def main():
    run = True

    enemy_images = [
        sprite_sheet.get_sprite(160, 0, 38, 43),
        sprite_sheet.get_sprite(40, 0, 38, 43),
        sprite_sheet.get_sprite(120, 0, 38, 43)
    ]

    player = Player(WIDTH / 2, HEIGHT - 60)

    enemies = []
    frames = 0
    waves = 3
    counter = 0
    time_to_spawn_enemy = 30
    time_to_enemy_shot = 40
    enemy_counter = 0
    pause_time = 200
    wave = 0
    pause = False
    score = 0
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        keys_pressed = pygame.key.get_pressed()
        draw_window()

        for bullet1, bullet2 in player.bullets:
            bullet1.draw()
            bullet1.update()
            bullet2.draw()
            bullet2.update()

        if enemy_counter < 10:
            counter = 0
            wave = 1
            pause = False

        if enemy_counter == 20:
            counter = 1
            wave = 2
            pause = True
            if frames % pause_time == 0:
                pause = False

        if enemy_counter == 30:
            counter = 2
            wave = 3
            pause = True
            if frames % pause_time == 0:
                pause = False

        if enemy_counter == 40:
            wave = 4
            pause = True

        if wave == 4 and pause == True and player.isAlive and len(enemies) == 0:
            draw_win()
            pygame.display.update()
            pygame.time.delay(5000)
            break
        else:

            if player.isAlive == False:
                break

            for bullet1, bullet2 in player.bullets:
                if bullet1.y < 0 and bullet2.y < 0: 
                    player.bullets.remove([bullet1, bullet2])

            if frames % time_to_spawn_enemy == 0 and pause == False:
                enemy_counter += 1
                x = random.randrange(0, WIDTH)
                enemy = Enemy(x, -50, enemy_images[counter])
                enemies.append(enemy)

            if frames % time_to_enemy_shot == 0 and pause == False:
                for enemy in enemies:
                    enemy.shot()

            for enemy in enemies:
                for bullet1, bullet2 in player.bullets:
                    if enemy.collison(bullet1, bullet2):
                        score += 10
                        if enemy in enemies: 
                            enemies.remove(enemy)

            for enemy in enemies:
                enemy.update()
                enemy.draw()
                for bull in enemy.bullets:
                    if player.collison(bull):
                        game_over()
                        pygame.display.update()
                        pygame.time.delay(1000)
                        player.isAlive = False
                    else:
                        bull.update()

                    bull.draw()

            draw_score(score)
            player.movement(keys_pressed)

        player.draw()
        player.update()
        frames += 1
        pygame.display.update()    
    pygame.quit()

main()
