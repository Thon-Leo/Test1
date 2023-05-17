'''
Function:
    飞扬的小鸟小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pickle
import random
import pygame
import time 
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import GameEndIterface, GameStartInterface, Bird, Pipe, rl



'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60 # 60
    # 屏幕大小
    SCREENSIZE = (288, 512)
    # 管道之间的空隙
    PIPE_GAP_SIZE = 100 # 上下gap大小 100
    # 标题
    TITLE = 'Flappy Bird —— Charles的皮卡丘'
    # 游戏声音路径
    SOUND_PATHS_DICT = {
        'die': os.path.join(rootdir, 'resources/audios/die.wav'),
        'hit': os.path.join(rootdir, 'resources/audios/hit.wav'),
        'point': os.path.join(rootdir, 'resources/audios/point.wav'),
        'swoosh': os.path.join(rootdir, 'resources/audios/swoosh.wav'),
        'wing': os.path.join(rootdir, 'resources/audios/wing.wav'),
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'number': {
            '0': os.path.join(rootdir, 'resources/images/0.png'), '1': os.path.join(rootdir, 'resources/images/1.png'),
            '2': os.path.join(rootdir, 'resources/images/2.png'), '3': os.path.join(rootdir, 'resources/images/3.png'),
            '4': os.path.join(rootdir, 'resources/images/4.png'), '5': os.path.join(rootdir, 'resources/images/5.png'),
            '6': os.path.join(rootdir, 'resources/images/6.png'), '7': os.path.join(rootdir, 'resources/images/7.png'),
            '8': os.path.join(rootdir, 'resources/images/8.png'), '9': os.path.join(rootdir, 'resources/images/9.png'),
        },
        'bird': {
            'red': {
                'up': os.path.join(rootdir, 'resources/images/redbird-upflap.png'),
                'mid': os.path.join(rootdir, 'resources/images/redbird-midflap.png'),
                'down': os.path.join(rootdir, 'resources/images/redbird-downflap.png')
            },
            'blue': {
                'up': os.path.join(rootdir, 'resources/images/bluebird-upflap.png'),
                'mid': os.path.join(rootdir, 'resources/images/bluebird-midflap.png'),
                'down': os.path.join(rootdir, 'resources/images/bluebird-downflap.png')
            },
            'yellow': {
                'up': os.path.join(rootdir, 'resources/images/yellowbird-upflap.png'),
                'mid': os.path.join(rootdir, 'resources/images/yellowbird-midflap.png'),
                'down': os.path.join(rootdir, 'resources/images/yellowbird-downflap.png')
            },
        },
        'background': {
            'day': os.path.join(rootdir, 'resources/images/background-day.png'),
            'night': os.path.join(rootdir, 'resources/images/background-night.png'),
        },
        'pipe': {
            'green': os.path.join(rootdir, 'resources/images/pipe-green.png'),
            'red': os.path.join(rootdir, 'resources/images/pipe-red.png'),
        },
        'others': {
            'gameover': os.path.join(rootdir, 'resources/images/gameover.png'),
            'message': os.path.join(rootdir, 'resources/images/message.png'),
            'base': os.path.join(rootdir, 'resources/images/base.png'),
        },
    }

time_passed = 1/Config.FPS
half_gap = Config.PIPE_GAP_SIZE/2

class Agent:
    def __init__(self):
        self.policy = dict()


    def init_policy(self):
        # for x in range(0, 180):
        #     for y in range(-100, 101):
        #         for z in range(-150, 151):
        #             self.policy[(x, y, z / 10)] = self.next_best_action(x, y, z / 10)
        for x in range(0, 180):
            for y in range(-100, 101):
                for z in range(-150, 151):
                    self.policy[(x, y, z / 10)] = self.best_act(x, y, z / 10)

    
    """ my code starts here """
    def will_colide(self, x: int, y: int, z: float):
        # every jump can raise about 30 pixels, 8 frames
        # inevitable collides
        if x <= 86 and (y <= -(half_gap-12) or y >= (half_gap-12)):
            return True
        else:
            # see if we will collide during moving up
            # c = 0
            while z > 0:
                # inevitable collides
                if x <= 86 and (y <= -(half_gap-12) or y >= (half_gap-12)):
                    return True
                # hit top or bot pipe
                # if x < 86 and (y < -(half_gap+32) or y > (half_gap+32)):
                # update and see if next frame will collide
                y += z
                x -= 4
                
                z -= 60 * time_passed
                
                # c+=1
            # while x > 0:

            while y > 0:
                if x <= 86 and (y <= -(half_gap-12) or y >= (half_gap-12)):
                    return True
                # hit top or bot pipe
                # if x < 86 and (y < -(half_gap+32) or y > (half_gap+32)):
                # update and see if next frame will collide
                y += z
                x -= 4
                z -= 60 * time_passed
                

        return False
    

    def best_act(self, x, y, z):
        flap_speed = max(12, z + 1)
        # if flap will collide?
        flap_speed -= 60 * time_passed
        flap_height = y + flap_speed

        # flap_speed -= 70 * time_passed
        # flap_height += flap_speed

        flap_b = self.will_colide(x-4, flap_height, flap_speed) # next frame

        # if idle will collide?
        idle_speed = z - 60 * time_passed
        idle_height = y + idle_speed
        idle_b = self.will_colide(x-4, idle_height, idle_speed) # next frame

        f_off = 1 if flap_b else 0
        i_off = 1 if idle_b else 0
        flap_value = -2000 * f_off - abs(flap_height)
        idle_value = -2000 * i_off - abs(idle_height)

        print(f"x: {x}, y: {y}, z: {z}")
        print(f"Idle collide? {idle_b}, flp collide? {flap_b}")
        if flap_value > idle_value:
            if x-4 <= 52 and not idle_b:
                print("False")
                return False
            print("True")
            return True
        print("False")
        return False


    def flap(self, bird, pipe_sprites):
        # distance
        pipe_top = pipe_sprites.sprites()[0]
        distance = pipe_top.rect.right - bird.rect.left

        if distance < 0:
            pipe_top = pipe_sprites.sprites()[2]
            distance = pipe_top.rect.right - bird.rect.left
        distance = min(distance, 179)
        
        # height
        if distance >= 179:
            height = 256 - bird.rect.centery
        else:
            height = pipe_top.rect.bottom + half_gap - bird.rect.centery
        if height < -100:
            height = -100
        elif height > 100:
            height = 100

        # speed
        # speed = round(bird.speed, 1) '''if bird.is_flapped else -round(bird.down_speed, 1)'''
        speed = round(bird.speed, 1)

        if speed > 15:
            speed = 15.0
        elif speed < -15:
            speed = -15.0

        # print(f"x, y, z: {distance, height, speed} \np: {self.policy[(distance,height,speed)]}") 

        # flspeed = 9 if speed < 0 else max(speed+1, 12)
        # flspeed = max(speed+1, 12)
        # flspeed -= 60 * time_passed
        # y = height+flspeed
        # flspeed-=1
        # y += flspeed
        # print(f"will flp collide? {self.will_colide(distance - 4, height, speed)}")
        print(f"Best act: {self.best_act(distance, height, speed)}")
        print()
        # print(f"will idle collide? {self.will_colide(distance, , speed-1)}")
        return self.policy[(distance,height,speed)]
    
    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def load(self, filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
            self.policy = data.policy


'''飞扬的小鸟小游戏'''
class FlappyBirdGame(PygameBaseGame):
    game_type = 'flappybird'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(FlappyBirdGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        timer = time.time()
        ag = Agent()
        
        path = r'D:\UIUC\Spring 23\games\cpgames\core\games\flappybird\q.pkl'
        a = False
        if a:
            ag.init_policy()
            ag.save(path)
        else:
            ag.load(path)


        while True:
            # 初始化
            screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
            # 定义游戏资源
            # --音频
            sounds = resource_loader.sounds
            # --数字图片
            number_images = resource_loader.images['number']
            for key in number_images: number_images[key] = number_images[key].convert_alpha()
            # --管道
            pipe_images = dict()
            pipe_images['bottom'] = random.choice(list(resource_loader.images['pipe'].values())).convert_alpha()
            pipe_images['top'] = pygame.transform.rotate(pipe_images['bottom'], 180)
            # --小鸟图片
            bird_images = random.choice(list(resource_loader.images['bird'].values()))
            for key in bird_images: bird_images[key] = bird_images[key].convert_alpha()
            # --背景图片
            backgroud_image = random.choice(list(resource_loader.images['background'].values())).convert_alpha()
            # --其他图片
            other_images = resource_loader.images['others']
            for key in other_images: other_images[key] = other_images[key].convert_alpha()
            # 游戏开始界面
            game_start_info = GameStartInterface(screen, sounds, bird_images, other_images, backgroud_image, cfg)
            # 进入主游戏
            score = 0
            bird_pos, base_pos, bird_idx = list(game_start_info.values())
            base_diff_bg = other_images['base'].get_width() - backgroud_image.get_width()
            clock = pygame.time.Clock()
            # --管道类
            pipe_sprites = pygame.sprite.Group()
            num_pipe = 2 # 此数越大 pipe越密集
            for i in range(num_pipe): 
                pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
                pipe_sprites.add(Pipe(image=pipe_images.get('top'), position=(cfg.SCREENSIZE[0]+200 +i*cfg.SCREENSIZE[0]/num_pipe, pipe_pos.get('top')[-1])))
                pipe_sprites.add(Pipe(image=pipe_images.get('bottom'), position=(cfg.SCREENSIZE[0]+200 +i*cfg.SCREENSIZE[0]/num_pipe, pipe_pos.get('bottom')[-1])))           
            # --bird类
            bird = Bird(images=bird_images, idx=bird_idx, position=bird_pos)
            # --是否增加pipe
            is_add_pipe = True
            # --游戏是否进行中
            is_game_running = True
            
            while is_game_running:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        QuitGame()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:

                            bird.setFlapped()
                            # sounds['wing'].play()

                # time.sleep(0.1)
                # pipe_top = pipe_sprites.sprites()[0]
                # distance = pipe_top.rect.left - bird.rect.left

                # if distance < 0:
                #     pipe_top = pipe_sprites.sprites()[2]
                #     distance = pipe_top.rect.left - bird.rect.left
                # distance = min(distance, 149)
                
                # # height
                # if distance >= 149:
                #     height = 190 - bird.rect.centery
                # else:
                #     height = pipe_top.rect.bottom + half_gap - bird.rect.centery
                # if height < -149:
                #     height = -149
                # elif height > 149:
                #     height = 149
                
                # speed = round(bird.up_speed, 1) if bird.is_flapped else -round(bird.down_speed, 1)

                if ag.flap(bird, pipe_sprites):
                    
                    bird.setFlapped()
                    print("\nflap ")
                    print()

                # --碰撞检测
                for pipe in pipe_sprites:
                    if pygame.sprite.collide_mask(bird, pipe):
                        # sounds['hit'].play()
                        is_game_running = False
                        
                # if is_game_running:
                #     a = 1+1
                #     # print(f"will collide? \n x, y, z: {distance, height, speed}, p = {ag.will_colide(distance,height,speed)}")
                # else:
                #     print(f"dead \n x, y, z: {distance, height, speed}, p = {ag.will_colide(distance,height,speed)}")

                # --更新小鸟
                boundary_values = [0, base_pos[-1]]
                is_dead = bird.update(boundary_values, float(clock.tick(cfg.FPS))/1000.)
                if is_dead:
                    # sounds['hit'].play()
                    is_game_running = False 


                # --移动base实现小鸟往前飞的效果
                base_pos[0] = -((-base_pos[0] + 4) % base_diff_bg)


                # --移动pipe实现小鸟往前飞的效果
                flag = False
                
                for pipe in pipe_sprites:
                    pipe.rect.left -= 4 # 移动pipe
                    if pipe.rect.centerx < bird.rect.centerx and not pipe.used_for_score: # 算分
                        pipe.used_for_score = True
                        score += 0.5
                        if '.5' in str(score):
                            sounds['point'].play()
                    if pipe.rect.left < 5 and pipe.rect.left > 0 and is_add_pipe: # 增加新的pipe
                        pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
                        pipe_sprites.add(Pipe(image=pipe_images.get('top'), position=pipe_pos.get('top')))
                        pipe_sprites.add(Pipe(image=pipe_images.get('bottom'), position=pipe_pos.get('bottom')))
                        is_add_pipe = False
                    elif pipe.rect.right < 0:
                        pipe_sprites.remove(pipe)
                        flag = True
                        


                if flag: is_add_pipe = True
                # --绑定必要的元素在屏幕上
                screen.blit(backgroud_image, (0, 0))
                pipe_sprites.draw(screen)
                screen.blit(other_images['base'], base_pos)
                self.showScore(cfg, screen, score, number_images)
                bird.draw(screen)
                pygame.display.update()
                clock.tick(cfg.FPS)

            GameEndIterface(screen, sounds, self.showScore, score, number_images, bird, pipe_sprites, backgroud_image, other_images, base_pos, cfg)
    
    
    '''显示当前分数'''
    @staticmethod
    def showScore(cfg, screen, score, number_images):
        digits = list(str(int(score)))
        width = 0
        for d in digits:
            width += number_images.get(d).get_width()
        offset = (cfg.SCREENSIZE[0] - width) / 2
        for d in digits:
            screen.blit(number_images.get(d), (offset, cfg.SCREENSIZE[1] * 0.1))
            offset += number_images.get(d).get_width()