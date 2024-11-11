from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
import game_framework

# Boy Run Speed
# 반드시 프레임 타임으로 값으 변경하자. +1 +2 이렇게 절대 금지
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour   마라톤 : 40km / 2h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Bird:

    def __init__(self):
        self.x, self.y = 10, 200
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Fly)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


class Fly:
    @staticmethod
    def enter(bird, e):
        bird.frame = 0
        #bird.x += bird.x * 5
        if bird.x < 1500:
            bird.dir, bird.face_dir, bird.action = 1, 1, 1
        else:
            bird.dir, bird.face_dir, bird.action = -1, -1, 0

    @staticmethod
    def exit(bird, e):
        pass


    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION* ACTION_PER_TIME * game_framework.frame_time) % 5
        # AF/S * time
        #boy.x += boy.dir * 5
        #boy.x += 속도(boy.dir*속력) *시간
        bird.x += bird.dir* RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(bird):
        if bird.face_dir > 0:
            bird.image.clip_draw(int(bird.frame) * 182, bird.action * 170, 180, 170, bird.x, bird.y)
        else :
            bird.image.clip_composite_draw(int(bird.frame) * 100, bird.action * 100, 100, 100, 0, 'v', bird.x, bird.y)