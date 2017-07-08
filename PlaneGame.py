#-*-coding:utf8-*-
import os,time,pygame,random
from pygame.locals import *

class Hero(pygame.sprite.Sprite):

    def __init__(self):
        super(Hero,self).__init__()
        self.img_name = 'hero1.png'
        self.image = pygame.image.load(self.img_name).convert_alpha()
        self.rect = self.image.get_rect(center=(240,780))
        self.hp = 100
        self.bomb_num = 0
    
    def update_image(self):
        if self.bomb_num == 0 :
            self.img_name = 'hero1.png'
        elif self.bomb_num == 5:
            self.img_name = hero_bomb1
        elif self.bomb_num == 10:
            self.img_name = hero_bomb2
        elif self.bomb_num == 15:
            self.img_name = hero_bomb3
        elif self.bomb_num == 20:
            self.img_name = hero_bomb4

        self.image = pygame.image.load(self.img_name).convert_alpha()
    #飞机的移动
    def update(self,key):
        if key == K_UP:
            self.rect.move_ip(0,-10)
        if key == K_LEFT:
            self.rect.move_ip(-10,0)
        if key == K_DOWN:
            self.rect.move_ip(0,10)
        if key == K_RIGHT:
            self.rect.move_ip(10,0)

        #不要超出屏幕外面
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 480:
            self.rect.right = 480
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 852:
            self.rect.bottom = 852

    #飞机的移动
    def move(self,directions):
        if directions[K_UP]:
            self.rect.move_ip(0,-12)
        if directions[K_LEFT]:
            self.rect.move_ip(-12,0)
        if directions[K_DOWN]:
            self.rect.move_ip(0,12)
        if directions[K_RIGHT]:
            self.rect.move_ip(12,0)

        #不要超出屏幕外面
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 480:
            self.rect.right = 480
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 852:
            self.rect.bottom = 852

    #飞机开火，开始发射子弹
    def fire(self):
        if fire_sure == True:
            #开始发射子弹
            bullet = Bullet(10,(self.rect.centerx,self.rect.midtop[1] - 10),'bullet1.png')
            bullets.add(bullet)
            everything.add(bullet)

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy,self).__init__()
        self.img_name = 'enemy1.png'
        self.image = pygame.image.load(self.img_name).convert_alpha()
        rando = random.randint(30,450)
        self.rect = self.image.get_rect(center=(rando,0))
        self.move_direction = 'Left' if random.randint(0,1) == 0 else 'Right' 
        self.bomb_num = 0
        self.hp = 100

    def update_image(self):
    
        if self.bomb_num == 0 :
            self.img_name = 'enemy1.png'
        elif self.bomb_num == 3:
            self.img_name = enemy_bomb1
        elif self.bomb_num == 6:
            self.img_name = enemy_bomb2
        elif self.bomb_num == 9:
            self.img_name = enemy_bomb3
        elif self.bomb_num == 12:
            self.img_name = enemy_bomb4

        self.image = pygame.image.load(self.img_name).convert_alpha()

    def move(self):
        speed_x = random.randint(5,10)
        speed_y = 5
        if self.move_direction == 'Left':
            self.rect.move_ip(-speed_x,speed_y)
        else:
            self.rect.move_ip(speed_x,speed_y)

        if self.rect.left <= 0:
            self.rect.left = 0
            self.move_direction = 'Right'
        if self.rect.right >= 480:
            self.rect.right = 480
            self.move_direction = 'Left'
        
    def fire(self):
        if (random.randint(1,60) == 8 or  random.randint(1,60) == 40) or (random.randint(1,60) == 20 or random.randint(1,60) == 30):
            bullet = Bullet(10,(self.rect.centerx,self.rect.midbottom[1] + 10),'bullet2.png',"Enemy")
            enemy_bullets.add(bullet)
            everything.add(bullet)

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self,shashangli,center_temp,name,juese_tmp='Hero'):
        super(Bullet,self).__init__()
        self.image = pygame.image.load(name).convert_alpha()
        self.shashangli = shashangli
        self.juese = juese_tmp
        self.rect = self.image.get_rect(center=center_temp)

    def move(self):
        if self.juese == 'Hero':
             self.rect.move_ip(0,-15)
        else:
            self.rect.move_ip(0,10)

        #如果超出了边界，那么回收子弹
        if self.rect.top <= 300 or self.rect.bottom >= 852 :
            if self.juese == 'Hero':
                bullets.remove(self)
            else:
                enemy_bullets.remove(self)
            self.kill


fire_sure = False  #是否开始开火 
game_status = 'UNKNOWN' #游戏状态，位置，开始，结束        
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()
everything = pygame.sprite.Group()
ADDENEMY = pygame.USEREVENT + 1

#爆炸图片
hero_bomb1 = 'hero_blowup_n1.png'
hero_bomb2 = 'hero_blowup_n2.png'
hero_bomb3 = 'hero_blowup_n3.png'
hero_bomb4 = 'hero_blowup_n4.png'

enemy_bomb1 = 'enemy1_down1.png'
enemy_bomb2 = 'enemy1_down2.png'
enemy_bomb3 = 'enemy1_down3.png'
enemy_bomb4 = 'enemy1_down4.png'
def main():

    '''游戏的入口'''
    pygame.init()
    pygame.mixer.init()

    window  = pygame.display.set_mode((480,852),pygame.RESIZABLE,32)
    window.fill((0,0,0))
    pygame.display.set_caption('飞机大战') 

    #定时刷新敌机
    pygame.time.set_timer(ADDENEMY,2000)
    #创建游戏的背景
    background = pygame.image.load('background.png').convert()
    begin = pygame.image.load('game_continue.png').convert_alpha()
    over = pygame.image.load('game_over.png').convert_alpha()


    hero = Hero()
    #死循环执行游戏
    running = True
    begin_bgm = True
    bullet_fire_num = 0
    while running:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                #elif event.key == K_UP:
                    #hero.update(event.key)
                #elif event.key == K_DOWN:
                    #hero.update(event.key)
                #elif event.key == K_LEFT:
                    #hero.update(event.key)
                #elif event.key == K_RIGHT:
                    #hero.update(event.key)
                elif event.key == K_SPACE:
                    if game_status == 'BEGIN':  
                        global fire_sure
                        fire_sure = True
                    hero.fire()
                elif event.key == K_RETURN:
                    global game_status
                    if game_status == 'UNKNOWN':
                        game_status = 'BEGIN'
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                if game_status == 'BEGIN':
                    enemy = Enemy()
                    everything.add(enemy)
                    enemys.add(enemy)


        window.blit(background,(0,0))
        #判断游戏状态
        if game_status == 'UNKNOWN':
            begin_rect = begin.get_rect(center=(240,426))
            window.blit(begin,begin_rect)
        elif game_status == 'BEGIN':

            if begin_bgm == True:
                if pygame.mixer.get_init():
                    pygame.mixer.music.load("DST-AngryMod.mp3")
                    pygame.mixer.music.set_volume(0.8)
                    pygame.mixer.music.play(-1)

            begin_bgm = False 
            keys = pygame.key.get_pressed()
            hero.move(keys) 
            bullet_fire_num += 1

            #英雄开火
            if bullet_fire_num % 5 == 0:
                 hero.fire()

            #英雄和敌机被子弹打中会爆炸
            bullet = pygame.sprite.spritecollideany(hero,enemy_bullets)
            if  bullet:
                 hero.hp -= 10
                 enemy_bullets.remove(bullet)
                 everything.remove(bullet)
           
            for enemy in enemys:
                enemy.fire()
                bul = pygame.sprite.spritecollideany(enemy,bullets)
                if bul:
                    bullets.remove(bul)
                    everything.remove(bul)
                    enemy.hp = 0
                    if pygame.mixer.get_init():
                        sound = pygame.mixer.Sound("Arcade Explo A.wav")
                        sound.set_volume(0.4)
                        sound.play(maxtime=1000)
                if enemy.hp == 0:
                    enemy.bomb_num += 1
                enemy.update_image()
                if enemy.bomb_num == 15:
                    everything.remove(enemy)
                    enemys.remove(enemy)
                    enemy.kill
            if hero.hp <= 0:
                hero.bomb_num += 1
                hero.kill
                if pygame.mixer.get_init():
                    sound = pygame.mixer.Sound('Arcade Explo A.wav')
                    sound.set_volume(0.5)
                    sound.play(maxtime=2000)
            hero.update_image()
            
            if hero.bomb_num == 30:
                game_status = 'Over'
            window.blit(hero.image,hero.rect)
            for entity in everything:
                entity.move()
                window.blit(entity.image,entity.rect)
        else:
            over_rect = begin.get_rect(center=(240,426))
            window.blit(over,over_rect)
            
            #结束音乐
            pygame.mixer.music.fadeout(4000)
            for entity in everything:
                entity.kill()
                everything.remove(entity)

        pygame.display.flip()
        time.sleep(0.02)

if __name__ == '__main__':
    main()
