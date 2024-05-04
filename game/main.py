import pygame
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.is_jump = False
        self.jump_count = 10
        self.health = 6
        self.walk_left = [
            pygame.image.load('images/player_left/player_left1.png'),
            pygame.image.load('images/player_left/player_left2.png'),
            pygame.image.load('images/player_left/player_left3.png'),
            pygame.image.load('images/player_left/player_left4.png'),
        ]
        self.walk_right = [
            pygame.image.load('images/player_right/player_right1.png'),
            pygame.image.load('images/player_right/player_right2.png'),
            pygame.image.load('images/player_right/player_right3.png'),
            pygame.image.load('images/player_right/player_right4.png'),
        ]
        self.player_anim_count = 0
        self.rect = self.walk_right[0].get_rect()
        self.rect.topleft = (x, y)
        self.action = 'idle'
        

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.action = 'left'
        elif keys[pygame.K_RIGHT] and self.x < 900:
            self.x += self.speed
            self.action = 'right'

        
        self.rect.x = self.x

    def jump(self, keys):
        if not self.is_jump:
            if keys[pygame.K_SPACE]:
                self.is_jump = True
        else:
            if self.jump_count >= -10:
                if self.jump_count > 0:
                    self.y -= (self.jump_count ** 2) / 2
                else:
                    self.y += (self.jump_count ** 2) / 2
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10

    def draw(self, screen, keys):
        self.player_anim_count = (self.player_anim_count + 1) % 4
        if self.action == 'left':
            screen.blit(self.walk_left[self.player_anim_count], (self.x, self.y))
        elif self.action == 'right':
            screen.blit(self.walk_right[self.player_anim_count], (self.x, self.y))
        else:
            
            screen.blit(self.walk_right[0], (self.x, self.y))            

        

class Boss(pygame.sprite.Sprite):
    def __init__(self, speed, x, y):
        super().__init__()
        self.images = [
            pygame.image.load('images/boss_left/boss_left1.png'),
            pygame.image.load('images/boss_left/boss_left2.png'),
            pygame.image.load('images/boss_left/boss_left3.png'),
            pygame.image.load('images/boss_left/boss_left4.png'),
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 1000  
        self.rect.y = randint(0, 0)
        self.x = x
        self.y = y  
        self.speed = speed
        self.animation_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (self.x, self.y)
        self.action = 'idle'
        


    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -150:
            self.kill()
        
        
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            
            
class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load('images/egg.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < +self.rect.height:
            self.kill()

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 563))
        pygame.display.set_caption("Птичий полет")
        self.bg = pygame.image.load('images/fon.png')
        self.hp_gf = pygame.image.load('images/hp.png')
        self.bg_rt = pygame.image.load('images/fon1.png')
        self.player_speed = 5
        self.bg_x = 0
        self.font = pygame.font.Font(None, 36)
        self.menu = True
        self.boss_spawn_delay = 3000
        self.last_boss_spawn_time = pygame.time.get_ticks()
        self.egg_group = pygame.sprite.Group()
        self.boss_kill_count = 0
        self.egg_kill_count = 0 

    def game_over(self):
        self.screen.fill((0, 0, 0))  
        self.draw_text("Конец игры", self.font, (255, 255, 255), self.screen, 500, 251)
        self.draw_text("Нажмите ESC, чтобы выйти из игры", self.font, (255, 255, 255), self.screen, 500, 281)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Выходим из метода, чтобы не продолжать игру
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False  # Выходим из цикла ожидания

    def run(self):
        while self.menu:
            self.screen.blit(self.bg_rt, (self.bg_x, 0))
            self.draw_text("Привет, друг.", self.font, (255, 255, 255), self.screen, 500, 251)
            self.draw_text("Нажми на ПРОБЕЛ, чтобы начать игру", self.font, (255, 255, 255), self.screen, 500, 281)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.menu = False

            pygame.display.update()

        running = True
        player = Player(350, 420, self.player_speed)
        bg_sound = pygame.mixer.Sound('sounds/walk.mp3')
        bg_sound.play(loops=100) 

        
        boss_group = pygame.sprite.Group()
        

        while running:
            self.screen.blit(self.bg, (self.bg_x, 0))
            self.screen.blit(self.bg, (self.bg_x + 1000, 0))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        egg = Egg(player.rect.centerx, player.rect.centery, 10)
                        self.egg_group.add(egg)


            player.move(keys)
            player.jump(keys)
            player.draw(self.screen,  keys)
            self.egg_group.update()
            self.egg_group.draw(self.screen)

            
            current_time = pygame.time.get_ticks()
            if current_time - self.last_boss_spawn_time > self.boss_spawn_delay:
                boss = Boss(10, 1000, randint(300, 300))
                boss_group.add(boss)
                self.last_boss_spawn_time = current_time

            
            boss_group.update()
            boss_group.draw(self.screen)
            

       
            collided_bosses = pygame.sprite.spritecollide(player, boss_group, True)
            for boss in collided_bosses:
                player.health -= 1
                self.boss_kill_count += 1
            if player.health <= 0:
                self.game_over()  
                running = False

            for egg in self.egg_group:
        
                collided_bosses = pygame.sprite.spritecollide(egg, boss_group, True)
        
            if collided_bosses:
                egg.kill()
                self.egg_kill_count += 1 

            self.bg_x -= 5
            if self.bg_x == -1000:
                self.bg_x = 0

            self.draw_health(player)

            pygame.display.update()
            self.clock.tick(20)

            

    def draw_health(self, player):
        x = 10
        for _ in range(player.health):
            self.screen.blit(self.hp_gf, (x, 40))
            x += 40
            self.draw_text(f'Киллы: {self.egg_kill_count}', self.font, (255, 255, 255), self.screen, 500, 80)
    
    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, 'white')
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)






if __name__ == "__main__":
    game = Game()
    game.run()
