
from pygame import *
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.SysFont('Arial', 70)
win = font.render('You win!', True, (0, 255, 0))
win = font.render('You lose1', True, (255, 0 ,0))

window = display.set_mode((700,500))
display.set_caption("Лабиринт")
background = transform.scale(image.load('background.jpg'), (700,500))

game = True
finish = False 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100,100))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_heigth):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.heigth = wall_heigth
        self.image = Surface((self.width,self.heigth ))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

w_1 = Wall(255, 230, 240, 340, 390, 59, 980)
w_2 = Wall(255, 230, 240, 540, 450, 50, 980)
w_3 = Wall(255, 230, 240, 390, 490, 50, 980)

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 300:
            self.direction = 'right'
        if self.rect.x > 650:
            self.direction = 'left'
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed


player = Player('hero.png', 5, 400, 4)
monster = Enemy('cyborg.png', 600, 280, 2)
treasure = GameSprite('treasure.png', 550, 400, 0)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background,(0,0))       
    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w_1) or sprite.collide_rect(player, w_2) or sprite.collide_rect(player, w_3 ):
        finish = True
        window.blit(lose, (200, 200))
        kick.play()
    if sprite.collide_rect(player, treasure):
        finish = True
        window.blit(win, (200, 200))
        money.play()

    window.blit(background, (0,0))
    w_1.draw_wall()
    w_2.draw_wall()
    w_3.draw_wall()
    player.reset()
    monster.reset()
    player.update()
    treasure.reset()
    display.update()
    time.delay(30)