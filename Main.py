#---------INITIAL SETUP
import pygame
#import pygame.surfarray
import sys
import os
from appdirs import user_data_dir
#import PowerPlantBattle
from collections import Counter
#import psutil
#import copy
import time
#import gc
#import random
import math
#import asyncio
import numpy as np
import pandas as pd
from collections import deque
import warnings
import csv
from collections import defaultdict
warnings.simplefilter(action='ignore', category=FutureWarning)

#gc.set_debug(gc.DEBUG_STATS)

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_TAB,
    KEYDOWN,
    KEYUP,
    QUIT,
)

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
#print(f"Joysticks detected: {joystick_count}")

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)  # grab the first controller
    joystick.init()
    #print(f"Controller name: {joystick.get_name()}")

# Set up display

info = pygame.display.Info()
#print("Monitor resolution:", info.current_w, "x", info.current_h)
monitor_width = info.current_w
monitor_height = info.current_h

target_ratio = 16 / 9
target_ratio_2 = 16/10
tolerance = 0.01 


if abs((monitor_width / monitor_height) - target_ratio) < tolerance:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 360
    scale_factor = int(monitor_width / SCREEN_WIDTH)
    screen = pygame.display.set_mode([SCREEN_WIDTH * scale_factor, SCREEN_HEIGHT * scale_factor], pygame.FULLSCREEN | pygame.DOUBLEBUF)
elif abs((monitor_width / monitor_height) - target_ratio_2) < tolerance:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 400
    scale_factor = int(monitor_width / SCREEN_WIDTH)
    screen = pygame.display.set_mode([SCREEN_WIDTH * scale_factor, SCREEN_HEIGHT * scale_factor], pygame.FULLSCREEN | pygame.DOUBLEBUF)
#force_windowed = True
#if force_windowed:
else:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 360
    scale_factor = int(monitor_width/SCREEN_WIDTH)
    screen = pygame.display.set_mode([SCREEN_WIDTH * scale_factor, SCREEN_HEIGHT * scale_factor], pygame.DOUBLEBUF)

print(scale_factor)
TARGET_FPS = 60

pygame.display.set_caption("Big Mode Game Jam 2026")

if getattr(sys, 'frozen', False):  # If running as a packaged executable
    PATH_START = sys._MEIPASS  # Temporary folder PyInstaller uses
else:
    PATH_START = os.path.dirname(__file__)  # Script folder

IMAGES_DICT = {}

def load_images_from_folder(base_path, folder_names, target_dict):
    for folder in folder_names:
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path):
            continue  # skip if folder doesn't exist

        folder_key = os.path.basename(folder_path)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                image_key = f"{folder_key}_{file}"
                base_surf = pygame.image.load(file_path).convert_alpha()
                target_dict[image_key] = pygame.transform.scale(
                    base_surf,
                    (round(base_surf.get_width() * scale_factor),
                    round(base_surf.get_height() * scale_factor))
                )


# Usage
#folders_to_load = ["UI", "Tiles", "Fonts", "Buildings", "Characters"]
folders_to_load = ["UI", "Tiles", "Fonts", "Buildings", "Ducky", "Weapons", "Enemies", "TalkingHead"]

load_images_from_folder(PATH_START, folders_to_load, IMAGES_DICT)

def load_font_letters():
    print()
    folder_path = os.path.join(PATH_START, "Fonts")
    full_white_font_image_path = os.path.join(folder_path, "monogram-bitmap_white.png")
    full__white_font_image_surf = pygame.image.load(full_white_font_image_path).convert_alpha()
    scaled_full__white_font_image_sur = pygame.transform.scale(
                    full__white_font_image_surf,
                    (round(full__white_font_image_surf.get_width() * scale_factor),
                    round(full__white_font_image_surf.get_height() * scale_factor))
    )
    full_black_font_image_path = os.path.join(folder_path, "monogram-bitmap.png")
    full__black_font_image_surf = pygame.image.load(full_black_font_image_path).convert_alpha()
    scaled_full__black_font_image_sur = pygame.transform.scale(
                    full__black_font_image_surf,
                    (round(full__white_font_image_surf.get_width() * scale_factor),
                    round(full__white_font_image_surf.get_height() * scale_factor))
    )
    char_map = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    for index, char in enumerate(char_map):
        x = (index % 16) * 6
        y = (index // 16) * 12 
        original_rect = (x, y, 6, 11)
        scaled_rect = tuple(int(v * scale_factor) for v in original_rect)
        white_letter_surf = scaled_full__white_font_image_sur.subsurface(pygame.Rect(scaled_rect))
        key = f"Letter_White_{char}"
        IMAGES_DICT[key] = white_letter_surf
        black_letter_surf = scaled_full__black_font_image_sur.subsurface(pygame.Rect(scaled_rect))
        key = f"Letter_Black_{char}"
        IMAGES_DICT[key] = black_letter_surf
    #custom_chars = {'elipses': (90, 60), 'selection': (24, 72)}
    original_rect = (90, 60, 6, 11)
    scaled_rect = tuple(int(v * scale_factor) for v in original_rect)
    white_letter_surf = scaled_full__white_font_image_sur.subsurface(pygame.Rect(scaled_rect))
    key = f"Letter_White_elipses"
    IMAGES_DICT[key] = white_letter_surf
    black_letter_surf = scaled_full__black_font_image_sur.subsurface(pygame.Rect(scaled_rect))
    key = f"Letter_Black_elipses"
    IMAGES_DICT[key] = black_letter_surf
    original_rect = (24, 72, 6, 11)
    scaled_rect = tuple(int(v * scale_factor) for v in original_rect)
    white_letter_surf = scaled_full__white_font_image_sur.subsurface(pygame.Rect(scaled_rect))
    key = f"Letter_White_selection"
    IMAGES_DICT[key] = white_letter_surf
    black_letter_surf = scaled_full__black_font_image_sur.subsurface(pygame.Rect(scaled_rect))
    key = f"Letter_Black_selection"
    IMAGES_DICT[key] = black_letter_surf

load_font_letters()

#icon_path_1 = os.path.join(PATH_START, "Buildings")
#icon_path_2 = os.path.join(icon_path_1, "Pumpkin.png")
#pygame.display.set_icon(pygame.image.load(icon_path_2))

#---------INDIVIDUAL SPRITE SET UP
class Individual_Sprite(pygame.sprite.Sprite):
    def __init__(self, image_key, subsurface_rect, start_pos, tile_number=None, uses_alpha=False):
        super().__init__()
        self.full_image = IMAGES_DICT[image_key]
        #Needs re-written for new logic
        if subsurface_rect is not None:
            subsurface_rect = tuple(int(v * scale_factor) for v in subsurface_rect)
            self.surf = self.full_image.subsurface(subsurface_rect)
        else:
            self.surf = self.full_image
        # Set rect from the scaled surface
        self.rect = self.surf.get_rect()

        # Scale starting position
        start_x = int(start_pos[1][0] * scale_factor)
        start_y = int(start_pos[1][1] * scale_factor)

        # Position the sprite
        self.start_pos_type = start_pos[0]
        if self.start_pos_type == 'tr':
            self.rect.topright = (start_x, start_y)
        elif self.start_pos_type == 'tl':
            self.rect.topleft = (start_x, start_y)
        elif self.start_pos_type == 'bl':
            self.rect.bottomleft = (start_x, start_y)
        elif self.start_pos_type == 'br':
            self.rect.bottomright = (start_x, start_y)

        # Store float positions
        self.world_x = float(self.rect.x)
        self.world_y = float(self.rect.y)
        self.world_rect = self.rect.copy()

        if uses_alpha:
            self.surf.set_alpha(0)
            self.surf.get_alpha()
            self.increase_alpha = True

        

    def update(self):
        global RUNTIME_STATE
        self.rect.x = int(self.world_x - RUNTIME_STATE["camera"].offset_x)
        self.rect.y = int(self.world_y - RUNTIME_STATE["camera"].offset_y)

    def fade_in(self):
        if self.increase_alpha:
            if TARGET_FPS == 60:
                amount_to_change = 5
            else:
                amount_to_change = 1
            curr_alpha = self.surf.get_alpha()
            curr_alpha += amount_to_change
            self.surf.set_alpha(curr_alpha)
            if curr_alpha >= 122:
                self.increase_alpha = False

    def fade_out(self):
        if self.decrease_alpha:
            if TARGET_FPS == 60:
                amount_to_change = 5
            else:
                amount_to_change = 1
            curr_alpha = self.surf.get_alpha()
            curr_alpha -= amount_to_change
            self.surf.set_alpha(curr_alpha)
            if curr_alpha <= 0:
                self.decrease_alpha = False

    


#---------INDIVIDUAL SPRITES
#This could be re-written around the new image logic. It may even need to be. 
class Regular_Font_Letter(Individual_Sprite):
    def __init__(self, letter, topright_input, recolor=True):
        self.letter = letter
        # Scale starting position
        start_x = int(topright_input[0] * scale_factor)
        start_y = int(topright_input[1] * scale_factor)
        self.topright_input = (start_x, start_y)
        if letter == 'DownArrow':
            full_image = IMAGES_DICT["Fonts_down_arrow.png"]
            self.curr_frame = 0
            self.animate_buffer = 0
            
            self.frame_1 = full_image.subsurface((0, 0, 8, 16))
            self.frame_2 = full_image.subsurface((0, 16, 8, 16))
            self.frame_3 = full_image.subsurface((0, 32, 8, 16))
            self.frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_2]

            base_surf = pygame.Surface((8, 16), pygame.SRCALPHA)
            base_surf.blit(self.frame_3, (0, 0))

        else:
            char_map = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
            custom_chars = {'elipses': (90, 60), 'selection': (24, 72)}
            if letter in custom_chars or letter in char_map:
                if recolor == True:
                    image_key = f"Letter_White_{letter}"
                else:
                    image_key = f"Letter_Black_{letter}"
        super().__init__(
            image_key=image_key,
            subsurface_rect=None,
            start_pos=['tl', (-400,-400)]
        )
        self.width = self.rect.width
        self.height = self.rect.height


    def reveal(self):
        self.rect.topright = self.topright_input

    def hide(self):
        self.rect.topright = (-400, -400) 
        


class Title_Screen(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_TitleScreen.png",
            subsurface_rect=None,
            start_pos=['tl', (0,0)]
        )

class Diner_Screen(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_diner_bg.png",
            subsurface_rect=None,
            start_pos=['tl', (0,0)]
        )

class Black_Screen(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_BlackScreen.png",
            subsurface_rect=None,
            start_pos=['tl', (0,0)]
        )
        self.increase_alpha = True
        self.decrease_alpha = False
        self.surf.set_alpha(0)

class Enemy_Alert(Individual_Sprite):
    def __init__(self, start_pos):
        super().__init__(
            image_key="UI_EnemyAlert.png",
            subsurface_rect=None,
            start_pos=['tl', start_pos]
        )

        self.start_time = pygame.time.get_ticks()

        self.HOLD_TIME = 500
        self.FADE_TIME = 500

        self.START_ALPHA = 122
        self.surf.set_alpha(self.START_ALPHA)

        self.dead = False

    def alert_slow_fade_out(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        # Phase 1: hold
        if elapsed < self.HOLD_TIME:
            return

        # Phase 2: fade
        fade_elapsed = elapsed - self.HOLD_TIME
        fade_ratio = min(fade_elapsed / self.FADE_TIME, 1.0)

        new_alpha = int(self.START_ALPHA * (1 - fade_ratio))
        self.surf.set_alpha(new_alpha)

        if fade_ratio >= 1.0:
            self.dead = True

class Level_Clear_Screen(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_LevelClear.png",
            subsurface_rect=None,
            start_pos=['tl', (0,0)]
        )

class Level_Clear_Continue_Screen(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_LevelClear_Continue.png",
            subsurface_rect=None,
            start_pos=['tl', (0,0)]
        )


class Game_Over_Screen(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_game over screen.png",
            subsurface_rect=None,
            start_pos=['tl', (0,0)]
        )

class Talking_Head(Individual_Sprite):
    def __init__(self, character):
        super().__init__(
            image_key=f"TalkingHead_{character}.png",
            subsurface_rect=None,
            start_pos=['tl', (400,100)]
        )
        self.character = character

class Tile(Individual_Sprite):
    def __init__(self, top_left, tile_number, df_pos=None):
        super().__init__(
            image_key=f"Tiles_{tile_number}.png",
            subsurface_rect=None,
            start_pos=['tl', top_left],
        )
        self.df_pos = df_pos
        if tile_number not in [4, 1, 3]:
            self.tile_number = 3
        else:
            self.tile_number = tile_number
        self.displayed_tile = str(tile_number)

class SpeedMeter(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key="UI_BodySpeedMeter.png",
            subsurface_rect=None,
            start_pos=['tl', (520,240)]
        )
        
class SpeedNeedle(Individual_Sprite):
    def __init__(self):
        super().__init__(
            image_key=f"UI_SpeadMeterNeddles_0.png",
            subsurface_rect=None,
            start_pos=['tl', (520,240)]
        )

class HP_Heart(Individual_Sprite):
    def __init__(self, top_left=(16, 16)):
        super().__init__(
            image_key="UI_Heart_01.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )
        self.dead = False
        self.frame = 1
        self.direction = 1
        self.frame_time = 400
        self.last_frame_tick = pygame.time.get_ticks()
        

    def animate_heart(self):
        if not self.dead:
            self.animate_heart_regular()
        else:
            self.animate_dead_heart()

    def start_dead_heart(self):
        self.dead = True
        self.dead_start_time = pygame.time.get_ticks()
        self.last_frame_tick = self.dead_start_time
        self.HOLD_TIME = 500
        self.FADE_TIME = 500
        frame_key = f"UI_HeartBreak.png"
        self.surf = IMAGES_DICT[frame_key].copy()
        self.START_ALPHA = 122

    def animate_dead_heart(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.dead_start_time

        # Phase 1: hold
        if elapsed < self.HOLD_TIME:
            return

        # Phase 2: fade
        fade_elapsed = elapsed - self.HOLD_TIME
        fade_ratio = min(fade_elapsed / self.FADE_TIME, 1.0)

        new_alpha = int(self.START_ALPHA * (1 - fade_ratio))
        self.surf.set_alpha(new_alpha)

        if fade_ratio >= 1.0:
            RUNTIME_STATE["dead_hearts_list"].remove(self)
            kill_and_delete(self)



    def animate_heart_regular(self):
        now = pygame.time.get_ticks()

        if now - self.last_frame_tick < self.frame_time:
            return

        self.last_frame_tick = now

        # Advance frame
        self.frame += self.direction

        # Bounce at ends
        if self.frame >= 3:
            self.frame = 3
            self.direction = -1
        elif self.frame <= 1:
            self.frame = 1
            self.direction = 1

        # Update sprite
        frame_key = f"UI_Heart_{self.frame:02d}.png"
        self.surf = IMAGES_DICT[frame_key]

class Overworld_Main_Text_box(Individual_Sprite):
    def __init__(self, top_left=(0,317)):
        super().__init__(
            image_key="UI_Textbox.png",
            subsurface_rect=(0,0,640,43),
            start_pos=['tl', top_left]
        )

class Overworld_Wide_Option_Box(Individual_Sprite):
    def __init__(self, top_left):
        super().__init__(
            image_key="UI_WideOptionBox.png",
            subsurface_rect=(0,0,208,43),
            start_pos=['tl', top_left]
        )

class Overworld_Wide_Option_Box_3(Individual_Sprite):
    def __init__(self, top_left):
        super().__init__(
            image_key=f"UI_WideOptionBox_3.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )

class Overworld_Wide_Option_Box_4(Individual_Sprite):
    def __init__(self, top_left):
        super().__init__(
            image_key=f"UI_WideOptionBox_4.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )


class Overworld_Wide_Option_Box_5(Individual_Sprite):
    def __init__(self, top_left):
        super().__init__(
            image_key=f"UI_WideOptionBox_5.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )

class Generic_Building(Individual_Sprite):
    def __init__(self, top_left, building, df_pos=None):
        super().__init__(
            image_key=f"Buildings_{building}.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )
        self.df_pos = df_pos
        self.building = building
        self.door_open = False

class Generic_Enemy(Individual_Sprite):
    def __init__(self, top_left, enemy_class, df_pos=None):
        if enemy_class == 'Fish':
            enemy_image = f"FishHole_01"
        elif enemy_class == 'Walrus':
            enemy_image = f"WalrusIdle_0_01"
        elif enemy_class != 'Test':
            enemy_image = f"{enemy_class}_90"
        else:
            enemy_image = enemy_class
        super().__init__(
            image_key=f"Enemies_{enemy_image}.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )
        self.df_pos = df_pos
        self.enemy_class = enemy_class
        if enemy_class == 'Fish':
            self.hp = 2
        else:
            self.hp = 2
        self.bullet = None
        self.last_shot_time = -3000
        self.direction = '90'
        self.previous_direction = '90'
        self.angle = 90.0
        self.vx = 0.0
        self.vy = 0.0
        self.bonk = False
        self.bonk_frame = 1
        self.bonk_start = None
        self.moving=False
        self.following_player=False
        self.active=False
        self.alert=None
        if self.enemy_class == 'Fish':
            self.state = 'Hole'
            self.state_frame = 1
            self.state_start_time = pygame.time.get_ticks()
            self.player_near = False
            self.player_side = 'Right'
            self.just_shot = False
        elif self.enemy_class == 'Walrus':
            self.state = 'Idle'
            self.state_frame = 1
            self.state_start_time = pygame.time.get_ticks()
        else:
            self.state = None

    def take_damage(self):
        self.hp -= RUNTIME_STATE["damage"]
        if self.hp <= 0:
            if self.enemy_class == 'Fish':
                if self.state != 'RIP':
                    full_image = IMAGES_DICT[f"Enemies_FishRIP_180_01_{self.player_side}.png"]
                    self.surf = full_image
                    self.state = 'RIP'
                    self.state_frame = 1
                    self.state_start_time = pygame.time.get_ticks()
                    RUNTIME_STATE["speed_mult"] += .1
                    if self.alert:
                        kill_and_delete(self.alert)
            elif self.enemy_class == 'Walrus':
                if self.state != 'RIP':
                    full_image = IMAGES_DICT[f"Enemies_WalrusRIP_0_01.png"]
                    self.surf = full_image
                    self.state = 'RIP'
                    self.state_frame = 1
                    self.state_start_time = pygame.time.get_ticks()
                    RUNTIME_STATE["speed_mult"] += .1
            else:
                RUNTIME_STATE["speed_mult"] += .1
                play_faint_sound()
                if self.alert:
                    kill_and_delete(self.alert)
                kill_and_delete(self)
        else:
            if self.enemy_class == 'Fish':
                full_image = IMAGES_DICT[f"Enemies_FishDamage_180_01_{self.player_side}.png"]
                self.surf = full_image
                self.state = 'Damage'
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()
            elif self.enemy_class == 'Walrus':
                full_image = IMAGES_DICT[f"Enemies_WalrusDamage_0_01.png"]
                self.surf = full_image
                self.state = 'Damage'
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()
            play_damage_sound()

    def determine_action(self):
        if self.enemy_class == 'Pigeon':
            self.follow_player()
        elif self.enemy_class == 'Fish':
            self.fish_action()
        elif self.enemy_class == 'Walrus':
            self.walrus_action()
        elif self.enemy_class == 'Sleepy':
            return
        else:
            self.fire_bullet()
        if self.alert:
            self.sync_alert()

    def walrus_action(self):
        print('walrus action')
        if self.state == 'RIP':
            curr_hole_frame = f"Enemies_WalrusRIP_0_{self.state_frame:02d}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 7)
            new_hole_frame = f"Enemies_WalrusRIP_0_{new_frame:02d}.png"
            if new_frame <= 6:
                if new_hole_frame != curr_hole_frame:
                    full_image = IMAGES_DICT[new_hole_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                play_faint_sound()
                kill_and_delete(self)
        elif self.state == 'Damage':
            curr_hole_frame = f"Enemies_WalrusDamage_0_{self.state_frame:02d}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 7)
            new_hole_frame = f"Enemies_WalrusDamage_0_{new_frame:02d}.png"
            if new_frame <= 6:
                if new_hole_frame != curr_hole_frame:
                    full_image = IMAGES_DICT[new_hole_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                full_image = IMAGES_DICT[f"Enemies_WalrusIdle_0_01.png"]
                self.surf = full_image
                self.state = 'Idle'
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()
        elif self.state == 'Idle':
            print('walrus idle')
            curr_hole_frame = f"Enemies_WalrusIdle_0_{self.state_frame:02d}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 7)
            new_hole_frame = f"Enemies_WalrusIdle_0_{new_frame:02d}.png"
            if new_frame <= 6:
                if new_hole_frame != curr_hole_frame:
                    full_image = IMAGES_DICT[new_hole_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                full_image = IMAGES_DICT[f"Enemies_WalrusIdle_0_01.png"]
                self.surf = full_image
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()


    def fish_action(self):
        self.fish_check_player_distance()
        if self.state != 'Idle':
            self.just_shot = False
        if self.state == 'RIP':
            curr_hole_frame = f"Enemies_FishRIP_180_{self.state_frame:02d}_{self.player_side}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 5)
            new_hole_frame = f"Enemies_FishRIP_180_{new_frame:02d}_{self.player_side}.png"
            if new_frame <= 4:
                if new_hole_frame != curr_hole_frame:
                    full_image = IMAGES_DICT[new_hole_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                play_faint_sound()
                kill_and_delete(self)
        elif self.state == 'Damage':
            curr_hole_frame = f"Enemies_FishDamage_180_{self.state_frame:02d}_{self.player_side}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 5)
            new_hole_frame = f"Enemies_FishDamage_180_{new_frame:02d}_{self.player_side}.png"
            if new_frame <= 4:
                if new_hole_frame != curr_hole_frame:
                    full_image = IMAGES_DICT[new_hole_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                full_image = IMAGES_DICT[f"Enemies_FishIdle_01_{self.player_side}.png"]
                self.surf = full_image
                self.state = 'Idle'
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()
        elif self.state == 'Hole':
            curr_hole_frame = f"Enemies_FishHole_{self.state_frame:02d}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 7)
            new_hole_frame = f"Enemies_FishHole_{new_frame:02d}.png"
            if new_frame <= 6:
                if new_hole_frame != curr_hole_frame:
                    full_image = IMAGES_DICT[new_hole_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                full_image = IMAGES_DICT[f"Enemies_FishHole_01.png"]
                self.surf = full_image
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()
        elif self.state == 'Idle':
            curr_idle_frame = f"Enemies_FishIdle_{self.state_frame:02d}_{self.player_side}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 7)
            new_idle_frame = f"Enemies_FishIdle_{new_frame:02d}_{self.player_side}.png"
            if new_frame <= 6:
                if new_idle_frame != curr_idle_frame:
                    if new_frame == 3:
                        if self.just_shot == False and new_frame >= self.state_frame:
                            angle = math.degrees(
                            math.atan2(
                                    -(RUNTIME_STATE["player"].world_y - self.world_y),
                                    RUNTIME_STATE["player"].world_x - self.world_x
                                )
                            ) % 360
                            rad = math.radians(angle)
                            dx = -math.cos(rad)
                            dy = math.sin(rad)

                            BULLET_SPEED = 80
                            if self.player_side == 'Right':
                                bullet_x = self.world_x + 10 * scale_factor
                            else:
                                bullet_x = self.world_x - 4 * scale_factor
                            bullet_y = self.world_y

                            bullet = Bullet(
                                top_left=(bullet_x/scale_factor, bullet_y/scale_factor),
                                bullet_dx=dx,
                                bullet_dy=dy,
                                speed=BULLET_SPEED,
                                bullet_type='Fish',
                                enemy=self
                            )

                            RUNTIME_STATE["overworld_sprites"].add(bullet, layer=20)
                            RUNTIME_STATE["bullets"].append(bullet)
                            play_fish_shoot_sound()
                            self.just_shot = True
                        else:
                            new_frame += 1
                            new_idle_frame = f"Enemies_FishIdle_{new_frame:02d}_{self.player_side}.png"
                            self.just_shot = False
                    full_image = IMAGES_DICT[new_idle_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                if self.player_near:
                    full_image = IMAGES_DICT[f"Enemies_FishIdle_01_{self.player_side}.png"]
                    self.surf = full_image
                    self.state_frame = 1
                    self.state_start_time = pygame.time.get_ticks()
                else:
                    full_image = IMAGES_DICT[f"Enemies_FishShot_01_{self.player_side}.png"]
                    self.surf = full_image
                    self.state = 'Shot'
                    self.state_frame = 1
                    self.state_start_time = pygame.time.get_ticks()
                    play_fish_dive_sound()
        elif self.state == 'Shot':
            curr_shot_frame = f"Enemies_FishShot_{self.state_frame:02d}_{self.player_side}.png"
            current_time = pygame.time.get_ticks()
            new_frame = min(int((current_time - self.state_start_time)/100) + 1, 13)
            new_shot_frame = f"Enemies_FishShot_{new_frame:02d}_{self.player_side}.png"
            if new_frame <= 6:
                if new_shot_frame != curr_shot_frame:
                    full_image = IMAGES_DICT[new_shot_frame]
                    self.surf = full_image
                    self.state_frame = new_frame
            else:
                full_image = IMAGES_DICT[f"Enemies_FishHole_01.png"]
                self.surf = full_image
                self.state = 'Hole'
                self.state_frame = 1
                self.state_start_time = pygame.time.get_ticks()

        

    def fish_check_player_distance(self):
        global RUNTIME_STATE
        if RUNTIME_STATE["player"].world_x < self.world_x:
            self.player_side = "Left"
        else:
            self.player_side = "Right"
        dx = RUNTIME_STATE["player"].world_x - self.world_x
        dy = RUNTIME_STATE["player"].world_y - self.world_y
        length = math.hypot(dx, dy)
        if length > 200 * scale_factor:
            self.player_near = False
            
        else:
            if self.state == 'Hole':
                self.alert = Enemy_Alert(start_pos=(self.world_x/scale_factor + 3, self.world_y/scale_factor +7))
                RUNTIME_STATE["overworld_sprites"].add(self.alert, layer=15)
                full_image = IMAGES_DICT[f"Enemies_FishIdle_01_{self.player_side}.png"]
                self.surf = full_image
                self.state_frame = 1
                play_fish_emerge_sound()
                self.state = 'Idle'
            self.player_near = True



    def sync_alert(self):
        if not self.alert:
            return

        self.alert.world_x = self.world_x + 3 * scale_factor
        self.alert.world_y = self.world_y - 15 * scale_factor
        self.alert.world_rect.topleft = (
            int(self.alert.world_x),
            int(self.alert.world_y)
        )
        if not self.alert.dead:
            self.alert.alert_slow_fade_out()
        else:
            kill_and_delete(self.alert)
            self.alert = None
            

    def character_moving_animation(self):
        #if not self.bonk:
        if self.direction != self.previous_direction:
            full_image = IMAGES_DICT[f"Enemies_{self.enemy_class}_{self.direction}.png"]
            self.surf = full_image
            self.previous_direction = self.direction


    def follow_player(self):
        global RUNTIME_STATE

        if self.enemy_class != 'Pigeon':
            return
        
        dx = RUNTIME_STATE["player"].world_x - self.world_x
        dy = RUNTIME_STATE["player"].world_y - self.world_y
        length = math.hypot(dx, dy)
        if length > 250 * scale_factor:
            self.following_player = False
            
        else:
            if not self.active:
                self.alert = Enemy_Alert(start_pos=(self.world_x/scale_factor + 3, self.world_y/scale_factor +7))
                RUNTIME_STATE["overworld_sprites"].add(self.alert, layer=15)
                play_alert_sound()
            self.active = True
            self.following_player = True
        if self.active:

            dt = RUNTIME_STATE["delta_time"]
            ROT_SPEED = 120
            ACCEL = 90
            if not self.following_player:
                ACCEL = 0
            MAX_SPEED = 300
            SIDE_DAMPING = 8
            TURN_DRAG = 0.5
            FRICTION = 0.995
            LOOK_AHEAD = 64
            AVOID_FORCE = 90
            speed = math.hypot(self.vx, self.vy)
            speed_ratio = min(speed / MAX_SPEED, 1)
            effective_rot = ROT_SPEED * (1 - 0.6 * speed_ratio)

            fx = math.cos(math.radians(self.angle))
            fy = -math.sin(math.radians(self.angle))

            probe_x = self.world_x + fx * LOOK_AHEAD
            probe_y = self.world_y + fy * LOOK_AHEAD

            avoid_turn = 0

            for building in RUNTIME_STATE["building_group"]:
                if building.world_rect.collidepoint(probe_x, probe_y):
                    # Determine which side to turn
                    bx, by = building.world_rect.center
                    ox = bx - self.world_x
                    oy = by - self.world_y

                    obstacle_angle = math.degrees(math.atan2(-oy, ox)) % 360
                    diff = angle_diff(obstacle_angle, self.angle)

                    # Turn away from obstacle
                    avoid_turn = -1 if diff > 0 else 1
                    break



            player = RUNTIME_STATE["player"]

            dx = player.world_x - self.world_x
            dy = player.world_y - self.world_y

            target_angle = math.degrees(math.atan2(-dy, dx)) % 360

            turn_error = angle_diff(target_angle, self.angle)


            #Determine rather to run left or right
            TURN_DEADZONE = 3 

            turn_dir = 0

            #Checking player
            if turn_error > TURN_DEADZONE:
                turn_dir -= 1
            elif turn_error < -TURN_DEADZONE:
                turn_dir += 1

            #Checking obstacled
            turn_dir += avoid_turn *  180  #Tuneable value

            self.angle += turn_dir * effective_rot * dt



            movement_angle = math.degrees(math.atan2(-self.vy, self.vx)) % 360

            #if keys["up"] or keys["joy_up"]:
            rad = math.radians(self.angle)
            self.vx += math.cos(rad) * ACCEL * dt
            self.vy -= math.sin(rad) * ACCEL * dt
            self.moving = True
            
            #Determine rather to stop or slow down
            #if keys["back"]:
            #    self.vx *= 0.975
            #    self.vy *= 0.975

            self.vx *= FRICTION
            self.vy *= FRICTION

            if avoid_turn != 0:
                self.vx *= 0.97
                self.vy *= 0.97

            speed = math.hypot(self.vx, self.vy)
            if speed > MAX_SPEED:
                scale = MAX_SPEED / speed
                self.vx *= scale
                self.vy *= scale
                speed = math.hypot(self.vx, self.vy)
            if speed > 0.01:
                # Facing direction vector
                fx = math.cos(math.radians(self.angle))
                fy = -math.sin(math.radians(self.angle))

                # Velocity normalized
                vx_n = self.vx / speed
                vy_n = self.vy / speed

                # Dot product: how aligned velocity is with facing
                alignment = vx_n * fx + vy_n * fy  # -1..1

                # Remove sideways velocity
                side_strength = max(0, 1 - alignment)

                self.vx -= vx_n * side_strength * SIDE_DAMPING * dt * speed
                self.vy -= vy_n * side_strength * SIDE_DAMPING * dt * speed

                turn_factor = abs(angle_diff(self.angle, movement_angle)) / 180

                self.vx *= 1 - turn_factor * TURN_DRAG * dt
                self.vy *= 1 - turn_factor * TURN_DRAG * dt

            if abs(self.vx) > 0.01 or abs(self.vy) > 0.01:
                self.moving = True
                self.move(self.vx, self.vy, speed=1, dt=dt)
            else:
                if self.active:
                    self.active = False


    def old_move(self, dx, dy, speed, dt):
        move_x = dx * speed * dt * 4
        move_y = dy * speed * dt * 4
        angle = self.angle % 360
        if 0 <= angle < 15:
            self.direction = '0'
        elif 15 <= angle < 45:
            self.direction = '30'
        elif 45 <= angle < 75:
            self.direction = '60'
        elif 75 <= angle < 105:
            self.direction = '90'
        elif 105 <= angle < 135:
            self.direction = '120'
        elif 135 <= angle < 165:
            self.direction = '150'
        elif 165 <= angle < 195:
            self.direction = '180'
        elif 195 <= angle < 225:
            self.direction = '210'
        elif 225 <= angle < 255:
            self.direction = '240'
        elif 255 <= angle < 285:
            self.direction = '270'
        elif 285 <= angle < 315:
            self.direction = '300'
        elif 315 <= angle < 345:
            self.direction = '330'
        else:
            self.direction = '0'

        test_rect = self.world_rect.copy()
        test_rect.topleft = (self.world_x - (move_x), self.world_y - (move_y))
        for building in RUNTIME_STATE["building_group"]:
            if test_rect.colliderect(building.world_rect):
                self.moving = False
                if abs(self.vx) + abs(self.vy) < 5:
                    
                    self.vx = sign(self.vx) * 7.5
                    self.vy = sign(self.vy) * 7.5
                else:
                    self.vx *= -7.5
                    self.vy *= -7.5
                error_selection_sound()
                break
        for enemy in RUNTIME_STATE["enemy_group"]:
            if enemy != self:
                if test_rect.colliderect(enemy.world_rect):
                    self.moving = False
                    if abs(self.vx) + abs(self.vy) < 5:
                    
                        self.vx = sign(self.vx) * 7.5
                        self.vy = sign(self.vy) * 7.5
                    else:
                        self.vx *= -7.5
                        self.vy *= -7.5
                    error_selection_sound()
                    break

        if test_rect.colliderect(RUNTIME_STATE["player"].world_rect):
            if not RUNTIME_STATE["player"].intangible:
                RUNTIME_STATE["player_hp"] -= 1
                RUNTIME_STATE["speed_mult"] = RUNTIME_STATE["min_speed_mult"]
                RUNTIME_STATE["player"].intangible = True
                RUNTIME_STATE["player"].intangible_frame = 1
                RUNTIME_STATE["player"].intangible_start = pygame.time.get_ticks()
            self.vx *= -3.5
            self.vy *= -3.5
            #kill_and_delete(self)

        self.character_moving_animation()
        if self.moving:
            self.world_x -= int(move_x)
            self.world_y -= int(move_y)
            self.world_rect.topleft = (
                int(self.world_x),
                int(self.world_y)
            )
        

    def fire_bullet(self):
        global RUNTIME_STATE
        if self.bullet:
            return
        else:
            FIRE_COOLDOWN = 3000  # 3 seconds
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= FIRE_COOLDOWN:
                self.last_shot_time = current_time
            else:
                return
            dx = RUNTIME_STATE["player"].world_x - self.world_x
            dy = RUNTIME_STATE["player"].world_y - self.world_y
            length = math.hypot(dx, dy)
            if length == 0 or length > 1600:
                return  # or skip shooting this frame


            angle = math.degrees(
                math.atan2(
                    -(RUNTIME_STATE["player"].world_y - self.world_y),
                    RUNTIME_STATE["player"].world_x - self.world_x
                )
            ) % 360
            rad = math.radians(angle)
            dx = -math.cos(rad)
            dy = math.sin(rad)

            BULLET_SPEED = 100

            bullet_x = self.world_x - (64 * dx)
            bullet_y = self.world_y - (64 * dy)

            self.bullet = Enemy_Bullet(
                top_left=(bullet_x/scale_factor, bullet_y/scale_factor),
                bullet_dx=dx,
                bullet_dy=dy,
                speed=BULLET_SPEED,
                enemy=self
            )

            RUNTIME_STATE["overworld_sprites"].add(self.bullet, layer=20)
            RUNTIME_STATE["bullets"].append(self.bullet)
            play_shoot_sound()

    def move(self, dx, dy, speed, dt):
        move_x = dx * speed * dt * 4
        move_y = dy * speed * dt * 4
        angle = self.angle % 360
        if 0 <= angle < 15:
            self.direction = '0'
        elif 15 <= angle < 45:
            self.direction = '30'
        elif 45 <= angle < 75:
            self.direction = '60'
        elif 75 <= angle < 105:
            self.direction = '90'
        elif 105 <= angle < 135:
            self.direction = '120'
        elif 135 <= angle < 165:
            self.direction = '150'
        elif 165 <= angle < 195:
            self.direction = '180'
        elif 195 <= angle < 225:
            self.direction = '210'
        elif 225 <= angle < 255:
            self.direction = '240'
        elif 255 <= angle < 285:
            self.direction = '270'
        elif 285 <= angle < 315:
            self.direction = '300'
        elif 315 <= angle < 345:
            self.direction = '330'
        else:
            self.direction = '0'

        test_rect = self.world_rect.copy()
        test_rect.topleft = (self.world_x - (move_x), self.world_y - (move_y))
        collided=False
        coll_speed = math.hypot(self.vx, self.vy)
        if test_rect.colliderect(RUNTIME_STATE["player"].world_rect) and not RUNTIME_STATE["player"].collision_already_applied and coll_speed != 0:
            # Normalize velocity
            #RUNTIME_STATE["player"].move(self.vx, self.vy, speed=1, dt=dt)
            vx_n = self.vx / coll_speed
            vy_n = self.vy / coll_speed

            dx_left   = test_rect.right - RUNTIME_STATE["player"].world_rect.left
            dx_right  = RUNTIME_STATE["player"].world_rect.right - test_rect.left
            dy_top    = test_rect.bottom - RUNTIME_STATE["player"].world_rect.top
            dy_bottom = RUNTIME_STATE["player"].world_rect.bottom - test_rect.top

            min_dx = min(dx_left, dx_right)
            min_dy = min(dy_top, dy_bottom)

            # Determine collision normal + resolve penetration
            if min_dx < min_dy:
                if dx_left < dx_right:
                    test_rect.right = RUNTIME_STATE["player"].world_rect.left
                    nx, ny = 1, 0
                else:
                    test_rect.left = RUNTIME_STATE["player"].world_rect.right
                    nx, ny = -1, 0
            else:
                if dy_top < dy_bottom:
                    test_rect.bottom = RUNTIME_STATE["player"].world_rect.top
                    nx, ny = 0, 1
                else:
                    test_rect.top = RUNTIME_STATE["player"].world_rect.bottom
                    nx, ny = 0, -1

            # Reflect ONLY if moving into surface
            dot = vx_n * nx + vy_n * ny
            if dot < 0:
                vx_n -= 5 * dot * nx
                vy_n -= 5 * dot * ny

                self.vx = vx_n * coll_speed
                self.vy = vy_n * coll_speed

                # Nudge out to avoid re-collision
                test_rect.x += nx
                test_rect.y += ny

            self.world_x = test_rect.x
            self.world_y = test_rect.y

                    
            collided=True
        for enemy in RUNTIME_STATE["enemy_group"]:
            #Need to add logic to bounce the enemy back too?
            if enemy != self:
                if test_rect.colliderect(enemy.world_rect):
                    coll_speed = math.hypot(self.vx, self.vy)
                    if coll_speed == 0:
                        break

                    # Normalize velocity
                    vx_n = self.vx / coll_speed
                    vy_n = self.vy / coll_speed

                    dx_left   = test_rect.right - enemy.world_rect.left
                    dx_right  = enemy.world_rect.right - test_rect.left
                    dy_top    = test_rect.bottom - enemy.world_rect.top
                    dy_bottom = enemy.world_rect.bottom - test_rect.top

                    min_dx = min(dx_left, dx_right)
                    min_dy = min(dy_top, dy_bottom)

                    # Determine collision normal + resolve penetration
                    if min_dx < min_dy:
                        if dx_left < dx_right:
                            test_rect.right = enemy.world_rect.left
                            nx, ny = 1, 0
                        else:
                            test_rect.left = enemy.world_rect.right
                            nx, ny = -1, 0
                    else:
                        if dy_top < dy_bottom:
                            test_rect.bottom = enemy.world_rect.top
                            nx, ny = 0, 1
                        else:
                            test_rect.top = enemy.world_rect.bottom
                            nx, ny = 0, -1

                    # Reflect ONLY if moving into surface
                    dot = vx_n * nx + vy_n * ny
                    if dot < 0:
                        vx_n -= 5 * dot * nx
                        vy_n -= 5 * dot * ny

                        self.vx = vx_n * coll_speed
                        self.vy = vy_n * coll_speed

                        # Nudge out to avoid re-collision
                        test_rect.x += nx
                        test_rect.y += ny

                    self.world_x = test_rect.x
                    self.world_y = test_rect.y

                    #if not self.shooting or (self.shooting and self.shoot_frame > 6): #Allow bonk to override cancellable portion of shooting
                    #self.bonk = True
                    #self.bonk_start = pygame.time.get_ticks()
                    
                    collided=True
        for building in RUNTIME_STATE["building_group"]:
            if test_rect.colliderect(building.world_rect):
                coll_speed = math.hypot(self.vx, self.vy)
                if coll_speed == 0:
                    break

                # Normalize velocity
                vx_n = self.vx / coll_speed
                vy_n = self.vy / coll_speed

                dx_left   = test_rect.right - building.world_rect.left
                dx_right  = building.world_rect.right - test_rect.left
                dy_top    = test_rect.bottom - building.world_rect.top
                dy_bottom = building.world_rect.bottom - test_rect.top

                min_dx = min(dx_left, dx_right)
                min_dy = min(dy_top, dy_bottom)

                # Determine collision normal + resolve penetration
                if min_dx < min_dy:
                    if dx_left < dx_right:
                        test_rect.right = building.world_rect.left
                        nx, ny = 1, 0
                    else:
                        test_rect.left = building.world_rect.right
                        nx, ny = -1, 0
                else:
                    if dy_top < dy_bottom:
                        test_rect.bottom = building.world_rect.top
                        nx, ny = 0, 1
                    else:
                        test_rect.top = building.world_rect.bottom
                        nx, ny = 0, -1

                # Reflect ONLY if moving into surface
                dot = vx_n * nx + vy_n * ny
                if dot < 0:
                    vx_n -= 5 * dot * nx
                    vy_n -= 5 * dot * ny

                    self.vx = vx_n * coll_speed
                    self.vy = vy_n * coll_speed

                    # Nudge out to avoid re-collision
                    test_rect.x += nx
                    test_rect.y += ny

                self.world_x = test_rect.x
                self.world_y = test_rect.y

                #if not self.shooting or (self.shooting and self.shoot_frame > 6): #Allow bonk to override cancellable portion of shooting
                #    self.bonk = True
                #    self.bonk_start = pygame.time.get_ticks()
                
                collided=True
                #break



        
        self.character_moving_animation()
        if not collided:
            if self.moving:
                self.world_x -= int(move_x)
                self.world_y -= int(move_y)
                self.world_rect.topleft = (
                    int(self.world_x),
                    int(self.world_y)
                )
                '''
                if self.alert:
                    self.alert.world_x -= int(move_x)
                    self.alert.world_y -= int(move_y)
                    self.alert.world_rect.topleft = (
                    int(self.alert.world_x),
                    int(self.alert.world_y)
                    )
                '''
        else:
            self.world_rect.topleft = (
                int(self.world_x),
                int(self.world_y)
            )
            error_selection_sound()





class Enemy_Bullet(Individual_Sprite):
    def __init__(self, top_left, bullet_dx, bullet_dy, speed, enemy):
        super().__init__(
            image_key=f"Weapons_Bullet.png",
            subsurface_rect=None,
            start_pos=['tl', top_left]
        )
        self.bullet_dx = bullet_dx
        self.bullet_dy = bullet_dy
        self.speed = speed
        self.enemy = enemy

    def bullet_action(self):
        self.move_bullet()

    def move_bullet(self):
        global RUNTIME_STATE
        move_x = self.bullet_dx * self.speed * RUNTIME_STATE["delta_time"] * 4
        move_y = self.bullet_dy * self.speed * RUNTIME_STATE["delta_time"] * 4

        test_rect = self.world_rect.copy()
        test_rect.topleft = (self.world_x - (move_x), self.world_y - (move_y))
        for building in RUNTIME_STATE["building_group"]:
            if test_rect.colliderect(building.world_rect):
                RUNTIME_STATE["bullets"].remove(self)
                self.enemy.bullet=None
                kill_and_delete(self)
                break
        for enemy in RUNTIME_STATE["enemy_group"]:
            if enemy != self.enemy:
                if test_rect.colliderect(enemy.world_rect):
                    RUNTIME_STATE["bullets"].remove(self)
                    self.enemy.bullet=None
                    kill_and_delete(self)
                    break
        if test_rect.colliderect(RUNTIME_STATE["player"].world_rect):
            RUNTIME_STATE["player_hp"] -= 1
            RUNTIME_STATE["speed_mult"] -= .1
            self.enemy.bullet=None
            RUNTIME_STATE["bullets"].remove(self)
            kill_and_delete(self)
        self.world_x -= int(move_x)
        self.world_y -= int(move_y)
        self.world_rect.topleft = (
            int(self.world_x),
            int(self.world_y)
        )

class Bullet(Individual_Sprite):
    def __init__(self, top_left, bullet_dx, bullet_dy, speed, bullet_type=None, enemy=None):
        if bullet_type==None:
            super().__init__(
                image_key=f"Weapons_Bullet.png",
                subsurface_rect=None,
                start_pos=['tl', top_left]
            )
            self.bullet_type = None
            self.enemy = None
        else:
            if bullet_type == 'Fish':
                super().__init__(
                    image_key=f"Weapons_FishBullet.png",
                    subsurface_rect=None,
                    start_pos=['tl', top_left]
                )
                self.bullet_type = 'Fish'
                self.enemy=enemy
        self.bullet_dx = bullet_dx
        self.bullet_dy = bullet_dy
        self.speed = speed
        self.contact = False
        self.contact_frame = 1
        self.contact_start = None

    def bullet_action(self):
        if not self.contact:
            self.move_bullet()
        else:
            self.contact_animation()


    def move_bullet(self):
        global RUNTIME_STATE
        move_x = self.bullet_dx * self.speed * RUNTIME_STATE["delta_time"] * 4
        move_y = self.bullet_dy * self.speed * RUNTIME_STATE["delta_time"] * 4

        test_rect = self.world_rect.copy()
        test_rect.topleft = (self.world_x - (move_x), self.world_y - (move_y))
        if self.bullet_type != None and test_rect.colliderect(RUNTIME_STATE["player"].world_rect):
            if not RUNTIME_STATE["player"].intangible:
                RUNTIME_STATE["player_hp"] -= 1
                RUNTIME_STATE["speed_mult"] -= .1
                RUNTIME_STATE["player"].intangible = True
                RUNTIME_STATE["player"].intangible_start = pygame.time.get_ticks()
            self.contact = True
            self.contact_start = pygame.time.get_ticks()
            play_collision_sound()
        #Add logic for hitting player here
        for building in RUNTIME_STATE["building_group"]:
            if test_rect.colliderect(building.world_rect):
                self.contact = True
                self.contact_start = pygame.time.get_ticks()
                play_building_collision_sound()
                break
        for enemy in RUNTIME_STATE["enemy_group"]:
            if enemy != self.enemy and not (enemy.enemy_class == 'Fish' and enemy.state == 'Hole'):
                if test_rect.colliderect(enemy.world_rect):
                    if self.bullet_type == None:
                        enemy.take_damage()
                    self.contact = True
                    self.contact_start = pygame.time.get_ticks()
                    play_collision_sound()
                    break
        self.world_x -= int(move_x)
        self.world_y -= int(move_y)
        self.world_rect.topleft = (
            int(self.world_x),
            int(self.world_y)
        )

    def contact_animation(self):
        curr_contact_frame = f"Weapons_Contact_{self.contact_frame:02d}.png"
        current_time = pygame.time.get_ticks()
        new_frame = int((current_time - self.contact_start)/50) + 1
        new_contact_frame = f"Weapons_Contact_{(new_frame):02d}.png"
        if new_frame <= 4:
            if new_contact_frame != curr_contact_frame:
                full_image = IMAGES_DICT[new_contact_frame]
                self.surf = full_image
                self.contact_frame = new_frame
        else:
            RUNTIME_STATE["bullets"].remove(self)
            kill_and_delete(self)



class Ducky_Sprite(Individual_Sprite):
    def __init__(self, df_pos=None):
        super().__init__(
            image_key="Ducky_90.png",
            subsurface_rect=None,
            start_pos=['tl', (320, 180)]
        )
        self.df_pos=df_pos
        self.check_buffer=0
        self.pixels_moved=0
        self.direction = '90'
        self.previous_direction = '90'
        self.moving = False
        self.curr_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.angle = 90.0
        self.vx = 0.0
        self.vy = 0.0
        self.bonk = False
        self.bonk_frame = 1
        self.bonk_start = None
        HITBOX_MARGIN = int(2 * scale_factor)
        self.world_rect.inflate_ip(
            -HITBOX_MARGIN,
            -HITBOX_MARGIN
        )
        self.shooting = False
        self.shoot_frame = 1
        self.shoot_start = None
        self.intangible = False
        self.intangible_frame = 1
        self.intangible_start = None
        self.frame_changed = False
        self.previous_surf = self.surf
        self.collision_already_applied = False
        self.dstar = ''
        self.previous_dstar = ''
        

    def character_moving_animation(self):
        if not self.bonk and not self.shooting:
            if self.direction != self.previous_direction or self.dstar != self.previous_dstar:
                full_image = IMAGES_DICT[f"Ducky_{self.direction}{self.dstar}.png"]
                self.surf = full_image
                self.previous_direction = self.direction
                self.frame_changed = True
            else:
                self.frame_changed = False
        elif self.bonk and not self.shooting: #Shooting is always given priority over bonk
            curr_bonk_frame = f"Ducky_Bonk_{self.direction}_{self.bonk_frame:02d}{self.previous_dstar}.png"
            current_time = pygame.time.get_ticks()
            new_frame = int((current_time - self.bonk_start)/100) + 1
            new_bonk_frame = f"Ducky_Bonk_{self.direction}_{(new_frame):02d}{self.dstar}.png"
            if new_frame <= 6:
                if new_bonk_frame != curr_bonk_frame:
                    full_image = IMAGES_DICT[new_bonk_frame]
                    self.surf = full_image
                    self.bonk_frame = new_frame
                    self.frame_changed = True
                else:
                    self.frame_changed = False
            else:
                full_image = IMAGES_DICT[f"Ducky_{self.direction}{self.dstar}.png"]
                self.surf = full_image
                self.previous_direction = self.direction
                self.bonk = False
                self.bonk_frame = 1
                self.bonk_start = None
                self.frame_changed = True
                RUNTIME_STATE["current_bonk_pulse"] = 5
        elif self.shooting:
            #curr_shoot_frame = f"Ducky_DuckShooting_{self.direction}_{self.bonk_frame:02d}.png" #This will be correct when all directions work
            curr_shoot_frame = f"Ducky_DuckShooting_{self.direction}_{self.shoot_frame:02d}{self.previous_dstar}.png"
            current_time = pygame.time.get_ticks()
            new_frame = int((current_time - self.shoot_start)/80) + 1
            new_shoot_frame = f"Ducky_DuckShooting_{self.direction}_{(new_frame):02d}{self.dstar}.png"
            if new_frame <= 6:
                if new_shoot_frame != curr_shoot_frame:
                    if new_frame == 2:
                        rad = math.radians(self.angle)
                        dx = math.cos(rad)
                        dy = -math.sin(rad)

                        bullet_x = self.world_x - (64 * dx)
                        bullet_y = self.world_y - (64 * dy)


                        #make the speed static 500 for now
                        bullet_speed_mult = max(int(math.hypot(RUNTIME_STATE["player"].vx, RUNTIME_STATE["player"].vy))/200, 1)
                        speed=350 * bullet_speed_mult
                        new_bullet = Bullet(
                            top_left=(bullet_x / scale_factor, bullet_y / scale_factor),
                            bullet_dx=dx,
                            bullet_dy=dy,
                            speed=speed
                        )

                        RUNTIME_STATE["overworld_sprites"].add(new_bullet, layer=20)
                        RUNTIME_STATE["bullets"].append(new_bullet)
                        play_shoot_sound()
                    full_image = IMAGES_DICT[new_shoot_frame]
                    self.surf = full_image
                    self.shoot_frame = new_frame
                    self.frame_changed = True
                else:
                    self.frame_changed = False
            else:
                full_image = IMAGES_DICT[f"Ducky_{self.direction}{self.dstar}.png"]
                self.surf = full_image
                self.previous_direction = self.direction
                self.shooting = False
                self.shoot_frame = 1
                self.shoot_start = None
                self.frame_changed = True
        if self.frame_changed == True:
            self.previous_surf = self.surf
        if self.intangible:
            current_frame = self.intangible_frame
            current_time = pygame.time.get_ticks()
            new_frame = int((current_time - self.intangible_start)/50) + 1
            if new_frame <= 60:
                if new_frame != current_frame:
                    if new_frame % 2 == 0:
                        self.previous_surf = self.surf
                        intangible_image = "Ducky_Intangible.png"
                        full_image = IMAGES_DICT[intangible_image]
                        self.surf = full_image
                        self.intangible_frame = new_frame
                    else:
                        self.intangible_frame = new_frame
                        self.surf = self.previous_surf
                        self.previous_surf = self.surf
            else:
                full_image = IMAGES_DICT[f"Ducky_{self.direction}{self.dstar}.png"]
                self.surf = full_image
                self.previous_direction = self.direction
                self.intangible = False
                self.intangible_frame = 1
                self.intangible_start = None
        



            

        
    def character_stop_moving(self):
        full_image = IMAGES_DICT[f"Ducky_{self.direction}{self.dstar}.png"]
        self.surf = full_image

    
    def check_dstar(self):
        speed = int(math.hypot(self.vx, self.vy))
        speed_adjusted = int(speed/2.78)
        snapped_speed = int(speed_adjusted // 45) * 45
        if snapped_speed >= 135 and not self.intangible:
        #if snapped_speed >= 135:
            self.previous_dstar = self.dstar
            self.dstar = '_DSTAR'
        else:
            self.previous_dstar = self.dstar
            self.dstar = ''
        #print(snapped_speed)
        #print(self.dstar)

    def check_move(self):
        self.collision_already_applied = False
        global RUNTIME_STATE
        keys = RUNTIME_STATE["pressed_keys"]
        self.moving = False

        dt = RUNTIME_STATE["delta_time"]
        if RUNTIME_STATE["speed_mult"] < RUNTIME_STATE["min_speed_mult"]:
            RUNTIME_STATE["speed_mult"] = RUNTIME_STATE["min_speed_mult"]
        ROT_SPEED = 150
        ACCEL = 300 * (RUNTIME_STATE["speed_mult"] ** RUNTIME_STATE["speed_mult"])
        MAX_SPEED = 1000 * RUNTIME_STATE["speed_mult"]
        SIDE_DAMPING = 6
        TURN_DRAG = 0.55
        FRICTION = 0.995
        speed = math.hypot(self.vx, self.vy)
        speed_ratio = min(speed / MAX_SPEED, 1)
        effective_rot = ROT_SPEED * (1 - 0.6 * speed_ratio)

        
        if keys["left"] or keys["joy_left"]:
            self.angle += effective_rot  * dt
        if keys["right"] or keys["joy_right"]:
            self.angle -= effective_rot  * dt


        movement_angle = math.degrees(math.atan2(-self.vy, self.vx)) % 360
        angle = self.angle % 360

        #if keys["up"] or keys["joy_up"]:
        rad = math.radians(self.angle)
        self.vx += math.cos(rad) * ACCEL * dt
        self.vy -= math.sin(rad) * ACCEL * dt
        self.moving = True
        
        if keys["back"] and not self.bonk: #Do not allow braking while bonking
            speed_bonus = RUNTIME_STATE["speed_mult"] - 1
            if speed_bonus >= 1.0:
                brake_mult = 0.999995
            elif speed_bonus >= 0.8:
                brake_mult = 0.99995
            elif speed_bonus >= 0.6:
                brake_mult = 0.9995
            elif speed_bonus >= 0.4:
                brake_mult = 0.995
            elif speed_bonus >= 0.2:
                brake_mult = 0.95
            elif speed_bonus >= 0:
                brake_mult = 0.85
            else:
                brake_mult = 0.85
            self.vx *= brake_mult
            self.vy *= brake_mult

        self.vx *= FRICTION
        self.vy *= FRICTION

        speed = math.hypot(self.vx, self.vy)
        if speed > MAX_SPEED:
            scale = MAX_SPEED / speed
            self.vx *= scale
            self.vy *= scale
            speed = math.hypot(self.vx, self.vy)
        if speed > 0.01:
            # Facing direction vector
            fx = math.cos(math.radians(self.angle))
            fy = -math.sin(math.radians(self.angle))

            # Velocity normalized
            vx_n = self.vx / speed
            vy_n = self.vy / speed

            # Dot product: how aligned velocity is with facing
            alignment = vx_n * fx + vy_n * fy  # -1..1

            # Remove sideways velocity
            side_strength = max(0, 1 - alignment)

            self.vx -= vx_n * side_strength * SIDE_DAMPING * dt * speed
            self.vy -= vy_n * side_strength * SIDE_DAMPING * dt * speed

            turn_factor = abs(angle_diff(self.angle, movement_angle)) / 180

            self.vx *= 1 - turn_factor * TURN_DRAG * dt
            self.vy *= 1 - turn_factor * TURN_DRAG * dt

        if abs(self.vx) > 0.01 or abs(self.vy) > 0.01:
            self.moving = True
            self.move(self.vx, self.vy, speed=1, dt=dt)

        if RUNTIME_STATE["just_pressed"] and RUNTIME_STATE["just_pressed"]["action"]:
            if not self.shooting or (self.shooting and self.shoot_frame > 2): #Allow animation cancelling after shooting
                self.shooting = True
                self.shoot_start = pygame.time.get_ticks()
                self.shoot_frame = 2 #In case of animation cancel
            
        RUNTIME_STATE["camera"].follow(self)

    def move(self, dx, dy, speed, dt):
        move_x = dx * speed * dt * 4
        move_y = dy * speed * dt * 4
        angle = self.angle % 360
        if 0 <= angle < 15:
            self.direction = '0'
        elif 15 <= angle < 45:
            self.direction = '30'
        elif 45 <= angle < 75:
            self.direction = '60'
        elif 75 <= angle < 105:
            self.direction = '90'
        elif 105 <= angle < 135:
            self.direction = '120'
        elif 135 <= angle < 165:
            self.direction = '150'
        elif 165 <= angle < 195:
            self.direction = '180'
        elif 195 <= angle < 225:
            self.direction = '210'
        elif 225 <= angle < 255:
            self.direction = '240'
        elif 255 <= angle < 285:
            self.direction = '270'
        elif 285 <= angle < 315:
            self.direction = '300'
        elif 315 <= angle < 345:
            self.direction = '330'
        else:
            self.direction = '0'

        test_rect = self.world_rect.copy()
        test_rect.topleft = (self.world_x - (move_x), self.world_y - (move_y))
        self.check_dstar()
        #Old logic
        #New logic
        collided=False
        for enemy in RUNTIME_STATE["enemy_group"]:
            #Need to add logic to bounce the enemy back too?
            if test_rect.colliderect(enemy.world_rect):
                coll_speed = math.hypot(self.vx, self.vy)
                if coll_speed <= 0:
                    break
                enemy.move(self.vx, self.vy, speed=1, dt=dt)

                # Normalize velocity
                vx_n = self.vx / coll_speed
                vy_n = self.vy / coll_speed

                dx_left   = test_rect.right - enemy.world_rect.left
                dx_right  = enemy.world_rect.right - test_rect.left
                dy_top    = test_rect.bottom - enemy.world_rect.top
                dy_bottom = enemy.world_rect.bottom - test_rect.top

                min_dx = min(dx_left, dx_right)
                min_dy = min(dy_top, dy_bottom)

                # Determine collision normal + resolve penetration
                if min_dx < min_dy:
                    if dx_left < dx_right:
                        test_rect.right = enemy.world_rect.left
                        nx, ny = 1, 0
                    else:
                        test_rect.left = enemy.world_rect.right
                        nx, ny = -1, 0
                else:
                    if dy_top < dy_bottom:
                        test_rect.bottom = enemy.world_rect.top
                        nx, ny = 0, 1
                    else:
                        test_rect.top = enemy.world_rect.bottom
                        nx, ny = 0, -1

                # Reflect ONLY if moving into surface
                dot = vx_n * nx + vy_n * ny
                if dot < 0:
                    if RUNTIME_STATE["current_bonk_pulse"] < 0:
                        RUNTIME_STATE["current_bonk_pulse"] = 0
                    vx_n -= RUNTIME_STATE["current_bonk_pulse"] * dot * nx
                    vy_n -= RUNTIME_STATE["current_bonk_pulse"] * dot * ny

                    self.vx = vx_n * coll_speed
                    self.vy = vy_n * coll_speed

                    # Nudge out to avoid re-collision
                    test_rect.x += nx
                    test_rect.y += ny

                self.world_x = test_rect.x
                self.world_y = test_rect.y

                if not self.shooting or (self.shooting and self.shoot_frame > 2): #Allow bonk to override cancellable portion of shooting
                    self.bonk = True
                    self.bonk_start = pygame.time.get_ticks()
                
                collided=True
                if self.dstar != '':
                    print('DSTAR COLLISION')
                    RUNTIME_STATE["player_hp"] += 1
                    enemy.take_damage()
                elif not self.intangible:
                    RUNTIME_STATE["player_hp"] -= 1
                    RUNTIME_STATE["speed_mult"] = RUNTIME_STATE["min_speed_mult"]
                    self.intangible = True
                    self.intangible_frame = 1
                    self.intangible_start = pygame.time.get_ticks()
                
        for building in RUNTIME_STATE["building_group"]:
            if test_rect.colliderect(building.world_rect):
                coll_speed = math.hypot(self.vx, self.vy)
                if coll_speed <= 0:
                    break

                # Normalize velocity
                vx_n = self.vx / coll_speed
                vy_n = self.vy / coll_speed

                dx_left   = test_rect.right - building.world_rect.left
                dx_right  = building.world_rect.right - test_rect.left
                dy_top    = test_rect.bottom - building.world_rect.top
                dy_bottom = building.world_rect.bottom - test_rect.top

                min_dx = min(dx_left, dx_right)
                min_dy = min(dy_top, dy_bottom)

                # Determine collision normal + resolve penetration
                if min_dx < min_dy:
                    if dx_left < dx_right:
                        test_rect.right = building.world_rect.left
                        nx, ny = 1, 0
                    else:
                        test_rect.left = building.world_rect.right
                        nx, ny = -1, 0
                else:
                    if dy_top < dy_bottom:
                        test_rect.bottom = building.world_rect.top
                        nx, ny = 0, 1
                    else:
                        test_rect.top = building.world_rect.bottom
                        nx, ny = 0, -1

                # Reflect ONLY if moving into surface
                dot = vx_n * nx + vy_n * ny
                if dot < 0:
                    if RUNTIME_STATE["current_bonk_pulse"] < 2:
                        RUNTIME_STATE["current_bonk_pulse"] = 2
                    vx_n -= RUNTIME_STATE["current_bonk_pulse"] * dot * nx
                    vy_n -= RUNTIME_STATE["current_bonk_pulse"] * dot * ny

                    self.vx = vx_n * coll_speed
                    self.vy = vy_n * coll_speed

                    # Nudge out to avoid re-collision
                    test_rect.x += nx
                    test_rect.y += ny

                self.world_x = test_rect.x
                self.world_y = test_rect.y

                if not self.shooting or (self.shooting and self.shoot_frame > 2): #Allow bonk to override cancellable portion of shooting
                    self.bonk = True
                    self.bonk_start = pygame.time.get_ticks()
                
                collided=True
                #break



        
        self.character_moving_animation()
        if not collided:
            if self.moving:
                self.world_x -= int(move_x)
                self.world_y -= int(move_y)
                self.world_rect.topleft = (
                    int(self.world_x),
                    int(self.world_y)
                )
        else:
            self.world_rect.topleft = (
                int(self.world_x),
                int(self.world_y)
            )
            self.collision_already_applied = True
            error_selection_sound()
            RUNTIME_STATE["speed_mult"] -= .01
            RUNTIME_STATE["current_bonk_pulse"] -= 1

            

#---------CAMERA
class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_w = SCREEN_WIDTH * scale_factor
        self.screen_h = SCREEN_HEIGHT * scale_factor

    def follow(self, target):
        self.offset_x = target.world_x - self.screen_w // 2
        self.offset_y = target.world_y - self.screen_h // 2

    

    

#---------SPRITE GROUPS
class Speedometer_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.body = SpeedMeter()
        self.needle = SpeedNeedle()
        self.add(self.body)
        self.add(self.needle)
        self.speed_degree = 0
        self.curr_text = Regular_Font_Line(input_string='000', text_type='immediate', special_top_left=False, ducky_mph=True)
        self.add(self.curr_text)

    def animate_speed(self):
        speed = int(math.hypot(RUNTIME_STATE["player"].vx, RUNTIME_STATE["player"].vy))
        speed_adjusted = int(speed/2.78)
        snapped_speed = int(speed_adjusted // 45) * 45
        if snapped_speed > 180:
            snapped_speed = 180
        if snapped_speed != self.speed_degree:
            frame_key = f"UI_SpeadMeterNeddles_{str(snapped_speed)}.png"
            self.needle.surf = IMAGES_DICT[frame_key]
            self.speed_degree = snapped_speed
        mph = speed * 450 / 5280
        if mph > 100:
            mph = 99.9
        
        self.change_curr_text(f"{mph:04.1f}")

    def change_curr_text(self, input_string):
        for s in self.curr_text:
            s.kill()
            del s
        self.curr_text = Regular_Font_Line(input_string=input_string, text_type='immediate', special_top_left=False, ducky_mph=True)
        self.add(self.curr_text)
        for sprite in self.curr_text:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=6)


class OtherUI_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.option_box = Overworld_Wide_Option_Box(top_left=(432,0))
        self.add(self.option_box)
        enemies_left = int(len(RUNTIME_STATE["enemy_group"]))
        input_string = f"SPEED MULT: {RUNTIME_STATE["speed_mult"]:.2f} ENEMIES LEFT: {enemies_left:02d}"
        self.curr_text = Regular_Font_Line(input_string=input_string, text_type='immediate', special_top_left=False, ducky_mph=True)
        self.add(self.curr_text)

    def change_curr_text(self):
        for s in self.curr_text:
            s.kill()
            del s
        enemies_left = int(len(RUNTIME_STATE["enemy_group"]))
        input_string = f"SPEED MULT: {RUNTIME_STATE["speed_mult"]:.2f} ENEMIES LEFT: {enemies_left:02d}"
        self.curr_text = Regular_Font_Line(input_string=input_string, text_type='immediate', special_top_left=False, ducky_mph=False, special_top_box=True)
        self.add(self.curr_text)
        for sprite in self.curr_text:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=6)



class Tileset_Group(pygame.sprite.Group):
    def __init__(self, tile_map):
        super().__init__()
        self.tiles_dict = {}
        self.tile_map = tile_map

        tile_size = 16
        start_x, start_y = -96, -80
        indexes_to_change = []
        for row_index, (_, row) in enumerate(tile_map.iterrows()):
            y = start_y + row_index * tile_size
            for col_index, column in enumerate(row):
                x = start_x + col_index * tile_size
                if str(column) not in ["1", "3", "4"]:
                    #print(column)
                    indexes_to_change.append([row_index, col_index])
                    
                curr_tile = Tile(
                    (x, y),
                    column,
                    df_pos=(row_index, col_index)  # <--- pass DataFrame coordinates
                )
                self.tiles_dict[f"{row_index}_{col_index}"] = curr_tile
                self.add(curr_tile)
        self.moving = False
        for index in indexes_to_change:
            self.tile_map.iat[index[0], index[1]] = 3


class Building_Group(pygame.sprite.Group):
    def __init__(self, tile_map):
        super().__init__()
        self.tiles_dict = {}
        self.tile_map = tile_map

        tile_size = 16
        start_x, start_y = -96, -80

        for row_index, (_, row) in enumerate(tile_map.iterrows()):
            y = start_y + row_index * tile_size
            for col_index, column in enumerate(row):
                if str(column) != "0" and str(column) != "Exit":
                    x = start_x + col_index * tile_size
                    curr_building = Generic_Building(
                        (x, y),
                        column,
                        df_pos=(row_index, col_index)  # <--- pass DataFrame coordinates
                    )
                    self.tiles_dict[f"{row_index}_{col_index}"] = curr_building
                    self.add(curr_building)

        self.moving = False

class Enemy_Group(pygame.sprite.Group):
    def __init__(self, tile_map):
        super().__init__()
        self.tiles_dict = {}
        self.tile_map = tile_map

        tile_size = 16
        start_x, start_y = -96, -80

        for row_index, (_, row) in enumerate(tile_map.iterrows()):
            y = start_y + row_index * tile_size
            for col_index, column in enumerate(row):
                if str(column) != "0" and str(column) != "Exit":
                    x = start_x + col_index * tile_size
                    curr_building = Generic_Enemy(
                        (x, y),
                        column,
                        df_pos=(row_index, col_index)  # <--- pass DataFrame coordinates
                    )
                    self.tiles_dict[f"{row_index}_{col_index}"] = curr_building
                    self.add(curr_building)

        self.moving = False
        

class Overworld_Menu(pygame.sprite.Group):
    def __init__(self, input_string, text_type, options=None, use_buy_sound=False, money_box=False, store_box=False, quantity_box=False, special_top_left=False):
        super(Overworld_Menu, self).__init__()
        if options:
            self.option_box = Overworld_Option_Box(top_left=(0,(SCREEN_HEIGHT-86)), options=options, use_buy_sound=use_buy_sound)
            self.add(self.option_box)
            self.number_of_option_boxes = 1
            self.previous_option_boxes = []
        else:
            self.option_box = None
            self.number_of_option_boxes = 0
        self.special_top_left = special_top_left
        if self.special_top_left:
            self.main_text_box = Overworld_Main_Text_box(top_left=(0,40))
        else:
            self.main_text_box = Overworld_Main_Text_box(top_left=(0, SCREEN_HEIGHT-43))
        self.curr_text = Regular_Font_Line(input_string=input_string, text_type=text_type, special_top_left=self.special_top_left)
        self.add(self.main_text_box)
        self.add(self.curr_text)
        self.info_box = None

    def update_curr_text(self):
        self.curr_text.update()

    def change_curr_text(self, input_string, text_type):
        for s in self.curr_text:
            s.kill()
            del s
        self.curr_text = Regular_Font_Line(input_string=input_string, text_type=text_type, special_top_left=self.special_top_left)
        self.add(self.curr_text)
        for sprite in self.curr_text:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=6)
    
    def update_option_box(self):
        self.option_box.update()

    def add_option_box(self, options):
        self.previous_option_boxes.append(self.option_box)
        self.option_box = Overworld_Option_Box(top_left=(208,(SCREEN_HEIGHT-86)), options=options)
        self.number_of_option_boxes += 1
        self.add(self.option_box)

    def add_info_box(self, options):
        if self.info_box:
            self.remove_info_box()
        self.info_box = Overworld_Option_Box(top_left=(416,(SCREEN_HEIGHT-86)), options=options, use_arrow=False)
        self.add(self.info_box)
        for sprite in self.info_box:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=5)

    def remove_info_box(self):
        for s in self.info_box:
            s.kill()
            del s
        self.info_box = None

    def remove_option_box(self):
        for s in self.option_box:
            s.kill()
            del s
        self.option_box = self.previous_option_boxes[-1]
        self.option_box.final_selection = None
        self.option_box.final_selection_text = None
        self.number_of_option_boxes -= 1
        global RUNTIME_STATE
        if RUNTIME_STATE["hover_building"] != None:
            if RUNTIME_STATE["hover_building"].building != "Nothing":
                RUNTIME_STATE["hover_building"].kill()
            del RUNTIME_STATE["hover_building"]
            RUNTIME_STATE["hover_building"] = None

class Overworld_Option_Box(pygame.sprite.Group):
    def __init__(self, top_left, options, use_buy_sound=False, use_arrow=True):
        super(Overworld_Option_Box, self).__init__()
        if len(options) == 2:
            menu_box_sprite = Overworld_Wide_Option_Box(top_left)
        elif len(options) == 3:
            top_left = (top_left[0], top_left[1] - 12)
            menu_box_sprite = Overworld_Wide_Option_Box_3(top_left)
        elif len(options) == 4:
            top_left = (top_left[0], top_left[1] - 24)
            menu_box_sprite = Overworld_Wide_Option_Box_4(top_left)
        elif len(options) == 5:
            top_left = (top_left[0], top_left[1] - 36)
            menu_box_sprite = Overworld_Wide_Option_Box_5(top_left)
        else:
            print(f'invalid number of options: {len(options)}')
        self.use_buy_sound = use_buy_sound
        self.options = options
        
        self.add(menu_box_sprite)
        self.curr_selection = 1
        self.final_selection = None
        self.final_selection_text = None

        self.build_options(top_left, options, use_arrow)
        self.curr_selection_text = self.options[self.curr_selection - 1]

    def build_options(self, top_left, options, use_arrow):
        self.option_characters_list = []
        start_x, start_y = top_left

        for i, (option_text) in enumerate(options):
            char_list = self.create_text_label(option_text, start_x + 8, start_y + 8 + (12*i), arrow=use_arrow, recolor=False)
            self.option_characters_list.append(char_list)

        # Hide all selections first
        if use_arrow:
            for i, char_list in enumerate(self.option_characters_list):
                char_list[0].hide()  # Hide the first character of each move (this assumes your move_char_lists structure is consistent)

            # Show the selected move
            if 1 <= self.curr_selection <= len(self.option_characters_list):
                self.option_characters_list[self.curr_selection - 1][0].reveal()  # Reveal the first character of the selected move

    def create_text_label(self, text, x, y, arrow=False, visible=True, recolor=False):
        char_list = []
        curr_width = x
        if arrow:
            temp_char = Regular_Font_Letter('selection', (curr_width, y), recolor=recolor)
            curr_width += 1
            char_list.append(temp_char)
        for char in text:
            temp_char = Regular_Font_Letter(char, (curr_width, y), recolor=recolor)
            curr_width += int(temp_char.width/scale_factor)
            char_list.append(Regular_Font_Letter(char, (curr_width, y), recolor=recolor))
        for item in char_list:
            self.add(item)
            if visible:
                item.reveal()
            else:
                item.hide()
        return char_list
    
    def update(self):
        self.get_selection_input()

    def clear_all_text(self):
        for char_list in self.option_characters_list:
            for char in char_list:
                char.kill()
                self.remove(char)

    def get_selection_input(self):
        global RUNTIME_STATE
        new_selection = None
        if RUNTIME_STATE["just_pressed"] != None:
            if RUNTIME_STATE["just_pressed"]["action"]:
                #if not self.use_buy_sound:
                #    select_sound()
                self.final_selection = self.curr_selection
                self.final_selection_text = self.options[self.final_selection - 1]
                #print(self.final_selection)
                #print(self.final_selection_text)
            else:
                if RUNTIME_STATE["just_pressed"]["up"] or RUNTIME_STATE["just_pressed"]["joy_up"]:
                    if self.curr_selection > 1:
                        new_selection = self.curr_selection - 1
                if RUNTIME_STATE["just_pressed"]["down"] or RUNTIME_STATE["just_pressed"]["joy_down"]:
                    if self.curr_selection < len(self.option_characters_list):
                        new_selection = self.curr_selection + 1
        if new_selection != None and new_selection != self.curr_selection and self.final_selection == None:
            self.option_characters_list[self.curr_selection - 1][0].hide()
            self.curr_selection = new_selection
            self.option_characters_list[self.curr_selection - 1][0].reveal()
            self.curr_selection_text = self.options[self.curr_selection - 1]
            change_selection_sound()

class Regular_Font_Line(pygame.sprite.Group):
    def __init__(self, input_string, text_type, special_top_left=False, ducky_mph=False, special_top_box=False):
        super(Regular_Font_Line, self).__init__()
        self.text_type = text_type
        self.special_top_left = special_top_left
        self.ducky_mph = ducky_mph
        self.special_top_box = special_top_box
        self.set_letters(input_string, self.text_type)
        self.reveal_speed = 20  # ms per letter (~25 letters/sec)
        self.last_reveal_time = pygame.time.get_ticks()
        
        

    def update(self):
        global RUNTIME_STATE
        if not self.all_letters_set:

            now = pygame.time.get_ticks()
            elapsed = now - self.last_reveal_time

            # Only reveal a letter every X milliseconds
            if elapsed >= self.reveal_speed:
                revealed_count = 0
                for item in self.char_list:
                    if item.rect.topright != item.topright_input:
                        item.reveal()
                        if item is self.arrow:
                            self.is_arrow_on_screen = True
                        if self.text_type != 'immediate':
                            break
                    else:
                        revealed_count += 1

                self.last_reveal_time = now  # reset timer

                if revealed_count >= self.expected_length:
                    self.all_letters_set = True

        if self.is_arrow_on_screen and self.arrow:
            self.arrow.animate_arrow()

        if RUNTIME_STATE["just_pressed"] and RUNTIME_STATE["just_pressed"]["action"]:
            #select_sound()
            if self.text_type == 'arrow' and self.is_arrow_on_screen:
                for sprite in self:
                    sprite.kill()
                self.ready_for_removal = True

            else:
                for item in self.char_list:
                    item.reveal()
                self.all_letters_set = True

        if self.text_type in ('not_arrow', 'immediate') and self.ready_for_removal:
            for sprite in self:
                sprite.kill()
            self.empty()  # Clear group explicitly

    def create_text_label(self, text, x, y, arrow=False, visible=False, recolor=False):
        char_list = []
        curr_width = x
        if arrow:
            temp_char = Regular_Font_Letter('selection', (curr_width, y), recolor=recolor)
            curr_width += 1
            char_list.append(temp_char)
        for char in text:
            temp_char = Regular_Font_Letter(char, (curr_width, y), recolor=recolor)
            curr_width += int(temp_char.width/scale_factor)
            char_list.append(Regular_Font_Letter(char, (curr_width, y), recolor=recolor))
        for item in char_list:
            self.add(item)
            if visible:
                item.reveal()
            else:
                item.hide()
        return char_list

    def set_letters(self, input_string, text_type):
        if self.special_top_box:
            input_string_split_at = 21
        else:
            input_string_split_at = 108
        if len(input_string) > input_string_split_at: #Need to adjust for new resolution(s)
            split_index = input_string.rfind(' ', 0, input_string_split_at)
            if split_index == -1:
                split_index = input_string_split_at  # no space found, hard split
            input_string_top = input_string[:split_index].strip()
            input_string_bottom = input_string[split_index:].strip()
            self.expected_length = len(input_string_top) + len(input_string_bottom)
        else:
            input_string_top = input_string
            self.expected_length = len(input_string_top)
            input_string_bottom = None
        
        # Clear existing sprites efficiently
        for sprite in self.sprites():
            sprite.kill()
        self.empty()
        self.input_string_top = input_string_top
        self.input_string_bottom = input_string_bottom
        # Update internal state
        self.text_type = text_type
        self.arrow = None
        self.ready_for_removal = False
        self.is_arrow_on_screen = False
        self.all_letters_set = False
        # Starting positions NEED ADJUSTED
        if self.special_top_left:
            starting_height_top = 47
            starting_height_bottom = 63
            starting_width = 15
        elif self.ducky_mph:
            starting_height_top = 288
            starting_height_bottom = 400
            starting_width = 546
        elif self.special_top_box:
            starting_height_top = 7
            starting_height_bottom = 23
            starting_width = 436
        else:
            starting_height_top = SCREEN_HEIGHT - 36
            starting_height_bottom = SCREEN_HEIGHT - 20
            starting_width = 15 #if text_type == 'immediate' else 24

        self.char_list = self.create_text_label(input_string_top, starting_width, starting_height_top)

        # Bottom line (if exists)
        if input_string_bottom:
            char_list_bottom = self.create_text_label(input_string_bottom, starting_width, starting_height_bottom)
            self.char_list.extend(char_list_bottom)
            self.input_string_bottom_len = len(input_string_bottom)
        else:
            self.input_string_bottom_len = 0

        # Add arrow if required
        if text_type == 'arrow':
            arrow_x = self.char_list[-1].rect.x + 14
            self.arrow = Regular_Font_Letter('DownArrow', (arrow_x, 138))
            self.char_list.append(self.arrow)
            self.add(self.char_list)

        if text_type == 'immediate':
            for item in self.char_list:
                item.reveal()


#---------FUNCTIONS
def get_move_vector():
    keys = RUNTIME_STATE["pressed_keys"]
    dx = 0
    dy = 0

    # Tiles move opposite to player input
    if keys["up"] or keys["joy_up"]:
        dy = 1   # moving tiles down = player moves up
    if keys["down"] or keys["joy_down"]:
        dy = -1  # moving tiles up = player moves down
    if keys["left"] or keys["joy_left"]:
        dx = 1   # moving tiles right = player moves left
    if keys["right"] or keys["joy_right"]:
        dx = -1  # moving tiles left = player moves right

    # Normalize diagonal movement
    if dx != 0 and dy != 0:
        magnitude = math.sqrt(dx**2 + dy**2)
        dx /= magnitude
        dy /= magnitude

    return dx, dy

def get_inputs():
    if RUNTIME_STATE["in_menu"] == True:
        RUNTIME_STATE["pressed_keys"] = None
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # If the Escape key is pressed, stop the loop
                # Detect any key press (only print if no other key is being held)
                if not RUNTIME_STATE["key_pressed"]:
                    #print("Key pressed:", event.key)
                    RUNTIME_STATE["key_pressed"] = True
                    RUNTIME_STATE["pressed_keys"] = pygame.key.get_pressed()
            elif event.type == KEYUP:
                # Reset the key_pressed flag when the key is released
                RUNTIME_STATE["key_pressed"]  = False

            # Handle the quit event
            elif event.type == pygame.QUIT:
                #print("Quit event triggered")
                RUNTIME_STATE["running"] = False

            #elif event.type == pygame.WINDOWFOCUSLOST:
            #    print("Window lost focus! Pausing unnecessary updates.")
    else:
        # Reset keys at the start of each frame (so releases are handled)
        DEAD_ZONE = 0.3  # Change this value to tweak sensitivity

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNTIME_STATE["running"] = False
            #elif event.type == pygame.WINDOWFOCUSLOST:
            #    print("Window lost focus! Pausing unnecessary updates.")

            # --- Keyboard input ---
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                keys = pygame.key.get_pressed()
                RUNTIME_STATE["pressed_keys"]["up"] = (keys[pygame.K_w] or keys[pygame.K_UP])
                RUNTIME_STATE["pressed_keys"]["down"] = (keys[pygame.K_s] or keys[pygame.K_DOWN])
                RUNTIME_STATE["pressed_keys"]["left"] = (keys[pygame.K_a] or keys[pygame.K_LEFT])
                RUNTIME_STATE["pressed_keys"]["right"] = (keys[pygame.K_d] or keys[pygame.K_RIGHT])
                RUNTIME_STATE["pressed_keys"]["action"] = keys[pygame.K_RETURN]
                RUNTIME_STATE["pressed_keys"]["back"] = keys[pygame.K_SPACE]
                RUNTIME_STATE["pressed_keys"]["pause"] = keys[pygame.K_ESCAPE]

            # --- Controller buttons ---
            elif event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
                is_pressed = event.type == pygame.JOYBUTTONDOWN
                #print(event.button)
                # X button (confirm)
                if event.button == 0:
                    RUNTIME_STATE["pressed_keys"]["action"] = is_pressed
                if event.button == 1:
                    RUNTIME_STATE["pressed_keys"]["back"] = is_pressed
                if event.button == 6:
                    RUNTIME_STATE["pressed_keys"]["pause"] = is_pressed

                # D-pad buttons (example mapping)
                elif event.button == 11:
                    RUNTIME_STATE["pressed_keys"]["up"] = is_pressed
                elif event.button == 14:
                    RUNTIME_STATE["pressed_keys"]["right"] = is_pressed
                elif event.button == 12:
                    RUNTIME_STATE["pressed_keys"]["down"] = is_pressed
                elif event.button == 13:
                    RUNTIME_STATE["pressed_keys"]["left"] = is_pressed

            # --- Controller D-Pad via Hat ---
            elif event.type == pygame.JOYHATMOTION:
                hat_x, hat_y = event.value  # Tuple, e.g. (1, 0), (0, -1)
                RUNTIME_STATE["pressed_keys"]["left"] = hat_x == -1
                RUNTIME_STATE["pressed_keys"]["right"] = hat_x == 1
                RUNTIME_STATE["pressed_keys"]["up"] = hat_y == 1
                RUNTIME_STATE["pressed_keys"]["down"] = hat_y == -1

            # --- Controller D-pad (usually axes 6/7 on DualSense) ---
            elif event.type == pygame.JOYAXISMOTION:
                # Axis 0 = X, Axis 1 = Y
                axis_val = event.value
                
                if event.axis == 0:  # Left/Right
                    if abs(axis_val) < DEAD_ZONE:
                        
                        RUNTIME_STATE["pressed_keys"]["joy_left"] = False
                        RUNTIME_STATE["pressed_keys"]["joy_right"] = False
                    if abs(axis_val) >= DEAD_ZONE:
                        RUNTIME_STATE["pressed_keys"]["joy_left"] = axis_val < -DEAD_ZONE
                        RUNTIME_STATE["pressed_keys"]["joy_right"] = axis_val > DEAD_ZONE

                elif event.axis == 1:  # Up/Down
                    if abs(axis_val) < DEAD_ZONE:
                        RUNTIME_STATE["pressed_keys"]["joy_up"] = False
                        RUNTIME_STATE["pressed_keys"]["joy_down"] = False
                    if abs(axis_val) >= DEAD_ZONE:
                        RUNTIME_STATE["pressed_keys"]["joy_up"] = axis_val < -DEAD_ZONE
                        RUNTIME_STATE["pressed_keys"]["joy_down"] = axis_val > DEAD_ZONE

def update_input_edges():
    global RUNTIME_STATE
    RUNTIME_STATE["just_pressed"] = {}
    for key, pressed in RUNTIME_STATE["pressed_keys"].items():
        prev = RUNTIME_STATE["prev_pressed_keys"].get(key, False)
        RUNTIME_STATE["just_pressed"][key] = (pressed and not prev)  # pressed this frame, not last
    #return just_pressed
    RUNTIME_STATE["prev_pressed_keys"] = RUNTIME_STATE["pressed_keys"].copy()

def kill_and_delete(object):
    object.kill()
    del object

def kill_menu_and_clear():
    global RUNTIME_STATE
    for s in RUNTIME_STATE["DinerTalkBox"]:
        s.kill()
        del s
    RUNTIME_STATE["DinerTalkBox"] = None

def angle_diff(a, b):
    return (a - b + 180) % 360 - 180

def sign(x):
    return (x > 0) - (x < 0)


def initialize_overworld():
    global RUNTIME_STATE
    if not RUNTIME_STATE["tileset_current"]:
        for sprite in RUNTIME_STATE["tileset_group"]:
            RUNTIME_STATE["overworld_sprites"].add(sprite, layer=1)
        for sprite in RUNTIME_STATE["building_group"]:
            RUNTIME_STATE["overworld_sprites"].add(sprite, layer=2)
        for sprite in RUNTIME_STATE["enemy_group"]:
            RUNTIME_STATE["overworld_sprites"].add(sprite, layer=3)
        RUNTIME_STATE["camera"] = Camera()
        RUNTIME_STATE["player"] = Ducky_Sprite()
        RUNTIME_STATE["overworld_sprites"].add(RUNTIME_STATE["player"], layer=6)

        RUNTIME_STATE["main_bottom_textbox"] = None

        #RUNTIME_STATE["TopStatusBar"] = Overworld_Menu(input_string=RUNTIME_STATE["top_display_string"], text_type='immediate', special_top_left=True)
        #for sprite in RUNTIME_STATE["TopStatusBar"]:
        #    RUNTIME_STATE["ui_sprites"].add(sprite, layer=6)
        FADE_TIME = 1000
        music_channel.fadeout(FADE_TIME)
        music_channel.play(battle_music_sound, loops=-1, fade_ms=FADE_TIME)
        RUNTIME_STATE["speed_meter"] = Speedometer_Group()
        for sprite in RUNTIME_STATE["speed_meter"]:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=5)
        RUNTIME_STATE["tileset_current"] = True
        RUNTIME_STATE["other_ui"] = OtherUI_Group()
        for sprite in RUNTIME_STATE["other_ui"]:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=5)

def update_top_display():
    global RUNTIME_STATE
    if RUNTIME_STATE["tileset_current"]:

        fps = f"{RUNTIME_STATE['FPS']:03d}"
        movement_angle = int(math.degrees(math.atan2(-RUNTIME_STATE["player"].vy, RUNTIME_STATE["player"].vx)) % 360)
        speed = int(math.hypot(RUNTIME_STATE["player"].vx, RUNTIME_STATE["player"].vy))
        enemies_left = int(len(RUNTIME_STATE["enemy_group"]))
        #display_str = f"FPS: {fps} INTERNAL RESOLUTION: {SCREEN_WIDTH}x{SCREEN_HEIGHT} ACTUAL RESOLUTION: {screen.get_width()}x{screen.get_height()} PLAYER POS: {int(RUNTIME_STATE["player"].world_x), int(RUNTIME_STATE["player"].world_y)} PLAYER SCREEN POS {RUNTIME_STATE["player"].rect.topleft} PLAYER DIRECTION {RUNTIME_STATE["player"].direction} PLAYER ANGLE {int((RUNTIME_STATE["player"].angle % 360)):03d}, MOVE ANGLE {movement_angle:03d} SPEED {speed:04d} SPEED MULT {RUNTIME_STATE["speed_mult"]:.2f}"
        display_str = f"HP: {RUNTIME_STATE["player_hp"]:02d} SPEED: {speed:04d} SPEED MULT: {RUNTIME_STATE["speed_mult"]:.2f} Enemies Left: {enemies_left:02d} Stage: {RUNTIME_STATE["level"]:02d} Damage: {RUNTIME_STATE["damage"]:02d}                                           FPS {fps} POS {int(RUNTIME_STATE["player"].world_x), int(RUNTIME_STATE["player"].world_y)} ANGLE {int((RUNTIME_STATE["player"].angle % 360)):03d} MOVE ANGLE {movement_angle:03d} INT.RES {SCREEN_WIDTH}x{SCREEN_HEIGHT} ACT.RES {screen.get_width()}x{screen.get_height()} SCALE {scale_factor}"
        if RUNTIME_STATE["top_display_string"] != display_str:
            RUNTIME_STATE["TopStatusBar"].change_curr_text(input_string=display_str, text_type='immediate')
            RUNTIME_STATE["top_display_string"] = display_str


def get_current_dialog():
    global RUNTIME_STATE
    dialog_list = RUNTIME_STATE["curr_dialog_tree"][RUNTIME_STATE["curr_dialog_tree_level"] - 1]
    print(dialog_list)
    text = dialog_list[0]
    if len(dialog_list) > 1:
        options = dialog_list[1]
    else:
        options = None
    if len(dialog_list) > 2:
        talking_head = dialog_list[2]
    else:
        talking_head = None
    return text, options, talking_head

def apply_selected_buff(buff):
    global RUNTIME_STATE
    #["+3 HP", "+.2 Min Speed Mult", "+1 Damage"]
    if buff == "+3 HP":
        RUNTIME_STATE["player_hp"] += 3
    elif buff == "+1 Damage":
        RUNTIME_STATE["damage"] += 1
    elif buff == "+.2 Min Speed Mult":
        RUNTIME_STATE["min_speed_mult"] += .2

def change_level_selection():
    global RUNTIME_STATE
    for s in RUNTIME_STATE["overworld_sprites"]:
        s.kill()
        del s
    RUNTIME_STATE["tileset_group"] = None
    RUNTIME_STATE["building_group"] = None
    RUNTIME_STATE["enemy_group"] = None
    maps_path = os.path.join(PATH_START, "Maps")
    level_path = os.path.join(maps_path, f"{str(RUNTIME_STATE["level"])}")
    backgroundtiles_path = os.path.join(level_path, "BackgroundTiles.txt")
    tile_map = pd.read_csv(backgroundtiles_path, sep='\t', header=None)
    buildingmap_path = os.path.join(level_path, "Buildings.txt")
    building_map_fromsheet = pd.read_csv(buildingmap_path, sep='\t', header=None)
    enemymap_path = os.path.join(level_path, "Enemy.txt")
    enemy_map_fromsheet = pd.read_csv(enemymap_path, sep='\t', header=None)


    RUNTIME_STATE["tileset_group"] = Tileset_Group(tile_map) #save this?
    RUNTIME_STATE["building_group"] = Building_Group(building_map_fromsheet) #save this?
    RUNTIME_STATE["enemy_group"] = Enemy_Group(enemy_map_fromsheet) #save this?
    RUNTIME_STATE["tileset_current"] = False
    initialize_overworld()




def parse_dialog_tsv(path):
    dialog_groups = defaultdict(list)

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            speech_id = int(row["Speech"]) - 1  # zero-based index
            line = row["Line"].strip()

            # Options
            if row["Options"].strip().lower() == "yes":
                options = ["+3 HP", "+.2 Min Speed Mult", "+1 Damage"]  # or placeholder like ["OPTION_1", "OPTION_2"]
            else:
                options = None

            # Talking head normalization
            talking_head = row["TalkingHead"]

            dialog_groups[speech_id].append([
                line,
                options,
                talking_head
            ])

    # Convert defaultdict → ordered list
    return [dialog_groups[i] for i in sorted(dialog_groups)]


def ui_animations():
    hearts = RUNTIME_STATE["hearts_list"]
    dead_hearts = RUNTIME_STATE["dead_hearts_list"]
    hp = RUNTIME_STATE["player_hp"]
    if hp > len(hearts):
        i = len(hearts)
        heart_start = 16 + (20 * len(hearts))
        while i < hp:
            curr_heart = HP_Heart(top_left=(heart_start,16))
            RUNTIME_STATE["hearts_list"].append(curr_heart)
            RUNTIME_STATE["ui_sprites"].add(curr_heart, layer=5)
            i = i + 1
            heart_start += 20

    for i in range(len(hearts) - 1, hp - 1, -1):
        heart = hearts[i]
        heart.start_dead_heart()

        dead_hearts.append(heart)
        hearts.pop(i)
    for heart in hearts:
        heart.animate_heart()
    for heart in dead_hearts:
        heart.animate_heart()
    if RUNTIME_STATE["speed_meter"] != None:
        RUNTIME_STATE["speed_meter"].animate_speed()
    if RUNTIME_STATE["other_ui"] != None:
        RUNTIME_STATE["other_ui"].change_curr_text()



#---------GAME PHASES
def titlescreen_phase():
    global RUNTIME_STATE
    if RUNTIME_STATE["title_screen"] == None:
        RUNTIME_STATE["title_screen"] = Title_Screen()
        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["title_screen"], layer=7)
    elif RUNTIME_STATE["just_pressed"] and RUNTIME_STATE["just_pressed"]["action"]:
        kill_and_delete(RUNTIME_STATE["title_screen"])
        RUNTIME_STATE["title_screen"] = Diner_Screen()
        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["title_screen"], layer=1)
        RUNTIME_STATE["current_phase"] = diner_phase
        RUNTIME_STATE["hearts_list"] = []
        i = 0
        heart_start = 16
        while i < RUNTIME_STATE["player_hp"]:
            curr_heart = HP_Heart(top_left=(heart_start,16))
            RUNTIME_STATE["hearts_list"].append(curr_heart)
            RUNTIME_STATE["ui_sprites"].add(curr_heart, layer=5)
            RUNTIME_STATE["dead_hearts_list"] = []
            i = i + 1
            heart_start += 20

        

def overworld_phase():
    global RUNTIME_STATE
    if not RUNTIME_STATE["tileset_current"]:
        RUNTIME_STATE["title_screen"] = None
        initialize_overworld()
    else:
        RUNTIME_STATE["player"].check_move()
        #if RUNTIME_STATE["player"].moving:
        for enemy in RUNTIME_STATE["enemy_group"]:
            enemy.determine_action()
        if RUNTIME_STATE["bullets"] != []:
            for bullet in RUNTIME_STATE["bullets"]:
                bullet.bullet_action()
        for entity in RUNTIME_STATE["overworld_sprites"]:
            entity.update()
        if RUNTIME_STATE["tileset_current"]:
            #Check for level clear
            if not RUNTIME_STATE["enemy_group"] and RUNTIME_STATE["player_hp"] > 0:
                #Go to Level Clear Phase
                RUNTIME_STATE["current_phase"] = levelclear_phase
                    #Add winning overlay
            elif RUNTIME_STATE["player_hp"] <= 0:
                #Go to Game Over Phase
                RUNTIME_STATE["current_phase"] = gameover_phase

def levelclear_phase():
    global RUNTIME_STATE
    if not RUNTIME_STATE["end_overlay"]:
        print('Level Clear!')
        RUNTIME_STATE["end_overlay"] = Level_Clear_Screen()
        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["end_overlay"], layer=9)
        RUNTIME_STATE["level_cleared_tick"] = pygame.time.get_ticks()
    if RUNTIME_STATE["level_cleared_tick"] != None:
        if RUNTIME_STATE["level_cleared_tick"] != 'Done':
            current_time = pygame.time.get_ticks()
            if current_time - RUNTIME_STATE["level_cleared_tick"] >= 750:
                kill_and_delete(RUNTIME_STATE["end_overlay"])
                RUNTIME_STATE["end_overlay"] = Level_Clear_Continue_Screen()
                RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["end_overlay"], layer=1)
                RUNTIME_STATE["level_cleared_tick"] = 'Done'
    if RUNTIME_STATE["level_cleared_tick"] == 'Done':
        if RUNTIME_STATE["just_pressed"] and RUNTIME_STATE["just_pressed"]["action"]:
            print('ENTER HIT ENTER HIT ENTER HIT')
            RUNTIME_STATE["level_cleared_tick"] = None
            if RUNTIME_STATE["bullets"] != []:
                for bullet in reversed(RUNTIME_STATE["bullets"]):
                    kill_and_delete(bullet)
                RUNTIME_STATE["bullets"] = []
            RUNTIME_STATE["current_phase"] = transition_phase

def transition_phase():
    global RUNTIME_STATE
    if not RUNTIME_STATE["black_screen"]:
        print('Transition_Phase!')
        RUNTIME_STATE["black_screen"] = Black_Screen()
        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["black_screen"], layer=9)
    else:
        if RUNTIME_STATE["black_screen"].increase_alpha:
            RUNTIME_STATE["black_screen"].fade_in()
            if not RUNTIME_STATE["black_screen"].increase_alpha:
                RUNTIME_STATE["black_screen"].decrease_alpha = True
                if RUNTIME_STATE["title_screen"] == None:
                    print('ADDING OVERLAY')
                    kill_and_delete(RUNTIME_STATE["end_overlay"])
                    RUNTIME_STATE["title_screen"] = Diner_Screen()
                    RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["title_screen"], layer=1)
                    RUNTIME_STATE["end_overlay"] = None
                    FADE_TIME = 1000
                    music_channel.fadeout(FADE_TIME)
                    music_channel.play(main_music_sound, loops=-1, fade_ms=FADE_TIME)
                    for sprite in RUNTIME_STATE["speed_meter"]:
                        kill_and_delete(sprite)
                    RUNTIME_STATE["speed_meter"] = None
                    for sprite in RUNTIME_STATE["other_ui"]:
                        kill_and_delete(sprite)
                    RUNTIME_STATE["other_ui"] = None
        elif RUNTIME_STATE["black_screen"].decrease_alpha:
            RUNTIME_STATE["black_screen"].fade_out()
        else:
            kill_and_delete(RUNTIME_STATE["black_screen"])
            RUNTIME_STATE["black_screen"] = None
            RUNTIME_STATE["current_phase"] = diner_phase

def diner_phase():
    global RUNTIME_STATE
    if not RUNTIME_STATE["DinerTalkBox"]:
        dialog, options, talking_head = get_current_dialog()
        if talking_head != None:
            if RUNTIME_STATE["curr_talking_head"] == None:
                RUNTIME_STATE["curr_talking_head"] = Talking_Head(character=talking_head)
                RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["curr_talking_head"], layer=2)
        RUNTIME_STATE["DinerTalkBox"] = Overworld_Menu(dialog, options=options, text_type='not_arrow')
        for sprite in RUNTIME_STATE["DinerTalkBox"]:
            RUNTIME_STATE["ui_sprites"].add(sprite, layer=3)
    if RUNTIME_STATE["DinerTalkBox"].curr_text.all_letters_set == False:
        #print('trying to update text')
        RUNTIME_STATE["DinerTalkBox"].update_curr_text()
    elif RUNTIME_STATE["DinerTalkBox"].option_box:
        RUNTIME_STATE["DinerTalkBox"].update_option_box()
        if RUNTIME_STATE["DinerTalkBox"].option_box.final_selection_text != None:
            print("apply final selection text")
            apply_selected_buff(RUNTIME_STATE["DinerTalkBox"].option_box.final_selection_text)
            RUNTIME_STATE["curr_dialog_tree_level"] += 1
            if RUNTIME_STATE["curr_dialog_tree_level"] <= len(RUNTIME_STATE["curr_dialog_tree"]):
                dialog, options, talking_head = get_current_dialog()
                kill_menu_and_clear()
                if talking_head != None:
                    print('add talking head here')
                    if RUNTIME_STATE["curr_talking_head"] == None:
                        print('added')
                        RUNTIME_STATE["curr_talking_head"] = Talking_Head(character=talking_head)
                        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["curr_talking_head"], layer=2)
                RUNTIME_STATE["DinerTalkBox"] = Overworld_Menu(dialog, options=options, text_type='not_arrow')
                for sprite in RUNTIME_STATE["DinerTalkBox"]:
                    RUNTIME_STATE["ui_sprites"].add(sprite, layer=3)
    else:
        if RUNTIME_STATE["just_pressed"] and RUNTIME_STATE["just_pressed"]["action"]:
            next_menu_sound()
            RUNTIME_STATE["curr_dialog_tree_level"] += 1
            if RUNTIME_STATE["curr_dialog_tree_level"] <= len(RUNTIME_STATE["curr_dialog_tree"]):
                dialog, options, talking_head = get_current_dialog()
                kill_menu_and_clear()
                if talking_head != None:
                    print('add talking head there')
                    if RUNTIME_STATE["curr_talking_head"] == None:
                        print('added')
                        RUNTIME_STATE["curr_talking_head"] = Talking_Head(character=talking_head)
                        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["curr_talking_head"], layer=2)
                RUNTIME_STATE["DinerTalkBox"] = Overworld_Menu(dialog, options=options, text_type='not_arrow')
                for sprite in RUNTIME_STATE["DinerTalkBox"]:
                    RUNTIME_STATE["ui_sprites"].add(sprite, layer=3)

            else:
                RUNTIME_STATE["level"] += 1
                RUNTIME_STATE["curr_dialog_tree"] = RUNTIME_STATE["main_dialog_tree"][RUNTIME_STATE["level"]]
                
                RUNTIME_STATE["current_phase"] = transition_back_to_stage_phase

def transition_back_to_stage_phase():
    global RUNTIME_STATE
    if not RUNTIME_STATE["black_screen"]:
        print('Transition_Phase!')
        RUNTIME_STATE["black_screen"] = Black_Screen()
        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["black_screen"], layer=9)
    else:
        if RUNTIME_STATE["black_screen"].increase_alpha:
            RUNTIME_STATE["black_screen"].fade_in()
            if not RUNTIME_STATE["black_screen"].increase_alpha:
                RUNTIME_STATE["black_screen"].decrease_alpha = True
                if RUNTIME_STATE["title_screen"] != None:
                    kill_and_delete(RUNTIME_STATE["title_screen"])
                    RUNTIME_STATE["title_screen"] = None
                if RUNTIME_STATE["curr_talking_head"] != None:
                    kill_and_delete(RUNTIME_STATE["curr_talking_head"])
                    RUNTIME_STATE["curr_talking_head"] = None
                kill_menu_and_clear()
                RUNTIME_STATE["DinerTalkBox"] = None
                RUNTIME_STATE["curr_dialog_tree_level"] = 1
                change_level_selection()
        elif RUNTIME_STATE["black_screen"].decrease_alpha:
            RUNTIME_STATE["black_screen"].fade_out()
        else:
            kill_and_delete(RUNTIME_STATE["black_screen"])
            RUNTIME_STATE["black_screen"] = None
            RUNTIME_STATE["current_phase"] = overworld_phase




def gameover_phase():
    global RUNTIME_STATE
    if not RUNTIME_STATE["end_overlay"]:
        print('Player defeated!')
        RUNTIME_STATE["end_overlay"] = Game_Over_Screen()
        RUNTIME_STATE["ui_sprites"].add(RUNTIME_STATE["end_overlay"], layer=9)


#---------VARIABLES


#Running state, variables that would not get saved to a .json
RUNTIME_STATE = {
"running": True,
"clock": pygame.time.Clock(),
"in_menu": False,
"current_phase": titlescreen_phase,
"FPS": 0,
"overworld_sprites": pygame.sprite.LayeredUpdates(),
"ui_sprites": pygame.sprite.LayeredUpdates(),
"key_pressed": False,
"title_screen": None,
"tileset_current": False,
"top_display_string": 'FPS: 42069',
"bullets": [],
"speed_mult": 1.0,
"player_hp": 7,
"end_overlay": None,
"level": 0, #should be 0
"level_cleared_tick": None,
"black_screen": None,
"DinerTalkBox": None,
"damage": 1,
"min_speed_mult": 1.00,
"current_bonk_pulse": 5
}

#Set maps
maps_path = os.path.join(PATH_START, "Maps")
'''

level_path = os.path.join(maps_path, f"{str(RUNTIME_STATE["level"])}")
backgroundtiles_path = os.path.join(level_path, "BackgroundTiles.txt")
tile_map = pd.read_csv(backgroundtiles_path, sep='\t', header=None)
buildingmap_path = os.path.join(level_path, "Buildings.txt")
building_map_fromsheet = pd.read_csv(buildingmap_path, sep='\t', header=None)
enemymap_path = os.path.join(level_path, "Enemy.txt")
enemy_map_fromsheet = pd.read_csv(enemymap_path, sep='\t', header=None)


RUNTIME_STATE["tileset_group"] = Tileset_Group(tile_map) #save this?
RUNTIME_STATE["building_group"] = Building_Group(building_map_fromsheet) #save this?
RUNTIME_STATE["enemy_group"] = Enemy_Group(enemy_map_fromsheet) #save this?
'''

RUNTIME_STATE["pressed_keys"] = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "joy_up": False,
    "joy_down": False,
    "joy_left": False,
    "joy_right": False,
    "action": False,
    "back": False,
    "pause": False
}

RUNTIME_STATE["prev_pressed_keys"] = RUNTIME_STATE["pressed_keys"].copy()


dialogtree_path = os.path.join(maps_path, "DialogTree.txt")


dialog_tree = parse_dialog_tsv(dialogtree_path)

RUNTIME_STATE["main_dialog_tree"] = dialog_tree
RUNTIME_STATE["curr_dialog_tree"] = RUNTIME_STATE["main_dialog_tree"][0]
RUNTIME_STATE["curr_dialog_tree_level"] = 1
RUNTIME_STATE["curr_talking_head"] = None
RUNTIME_STATE["TopStatusBar"] = None
RUNTIME_STATE["speed_meter"] = None
RUNTIME_STATE["other_ui"] = None



#---------SOUND EFFECTS

SFX_DICT = {}

def load_sfx_from_folder(base_path, folder_names, target_dict):
    for folder in folder_names:
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path):
            continue  # skip if folder doesn't exist

        folder_key = os.path.basename(folder_path)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                image_key = f"{folder_key}_{file}"
                target_dict[image_key] = pygame.mixer.Sound(file_path)

# Usage
folders_to_load = ["SFX"]

load_sfx_from_folder(PATH_START, folders_to_load, SFX_DICT)

def walking_sound():
    if not walking_sfx_channel.get_busy():
        walking_sfx_channel.play(SFX_DICT["SFX_Walk.wav"])

def exit_all_menus_sound():
    #if not menu_sfx_channel.get_busy():
    menu_sfx_channel.play(SFX_DICT["SFX_ExitAllMenus.wav"])

def next_menu_sound():
    #if not menu_sfx_channel.get_busy():
    menu_sfx_channel.play(SFX_DICT["SFX_NextMenu.wav"])

def final_confirm_sound():
    menu_sfx_channel.play(SFX_DICT["SFX_FinalConfirm.wav"])

def change_selection_sound():
    menu_sfx_channel.play(SFX_DICT["SFX_ChangeSelection.wav"])

def error_selection_sound():
    menu_sfx_channel.play(SFX_DICT["SFX_Error.wav"])

def play_damage_sound():
    damage_channel.play(SFX_DICT["SFX_faint 02.wav"])

def play_faint_sound():
    faint_channel.play(SFX_DICT["SFX_high damage_faint 02.wav"])

def play_fish_shoot_sound():
    gunshot_channel.play(SFX_DICT["SFX_FishShot.wav"])

def play_shoot_sound():
    gunshot_channel.play(SFX_DICT["SFX_gunshot_replace.mp3"])

def play_alert_sound():
    alert_channel.play(SFX_DICT["SFX_PigeonAlert.wav"])

def play_fish_emerge_sound():
    alert_channel.play(SFX_DICT["SFX_FishEmerge.wav"])

def play_fish_dive_sound():
    alert_channel.play(SFX_DICT["SFX_FishDive.wav"])

def play_collision_sound():
    collision_channel.play(SFX_DICT["SFX_Collision.wav"])

def play_building_collision_sound():
    collision_channel.play(SFX_DICT["SFX_BuildingCollision.wav"])

#---------MUSIC
music_channel = pygame.mixer.Channel(0)

music_folder_path = os.path.join(PATH_START, "Music") #Music regularly
battle_music_path = os.path.join(music_folder_path, "Ducky fight sketch 04_02_26.mp3")
battle_music_sound = pygame.mixer.Sound(battle_music_path)
main_theme_path = os.path.join(music_folder_path, "Main theme sketch 03_02_26.mp3")
main_music_sound = pygame.mixer.Sound(main_theme_path)

music_channel.play(main_music_sound, loops=-1)  # loops=-1 for infinite loop
menu_sfx_channel = pygame.mixer.Channel(1)  # Find an available channel
walking_sfx_channel = pygame.mixer.Channel(2)
damage_channel = pygame.mixer.Channel(3)
faint_channel = pygame.mixer.Channel(4)
gunshot_channel = pygame.mixer.Channel(5)
alert_channel = pygame.mixer.Channel(6)
collision_channel = pygame.mixer.Channel(7)
gunshot_channel.set_volume(0.6)

#---------MAIN LOGIC
def main():
    global RUNTIME_STATE
    last_frame_time = time.time()
    screen.set_alpha(None)
    while RUNTIME_STATE["running"]:
        frame_start = time.time()
        RUNTIME_STATE["delta_time"] = frame_start - last_frame_time


        
        last_frame_time = frame_start
        get_inputs()
        update_input_edges()

        RUNTIME_STATE["current_phase"]()

        if not RUNTIME_STATE["end_overlay"]: #This is just for now, at a certain point we'll change this to be a phase
            if RUNTIME_STATE["speed_mult"] < RUNTIME_STATE["min_speed_mult"]:
                RUNTIME_STATE["speed_mult"] = RUNTIME_STATE["min_speed_mult"]
            if RUNTIME_STATE["TopStatusBar"] and RUNTIME_STATE["tileset_current"]:
                update_top_display()
            if RUNTIME_STATE["current_phase"] != titlescreen_phase:
                ui_animations()

        
        
        # Clear the screen
        #render_start = time.time()
        for entity in RUNTIME_STATE["overworld_sprites"]:
            screen.blit(entity.surf, entity.rect)

        for entity in RUNTIME_STATE["ui_sprites"]:
            screen.blit(entity.surf, entity.rect)

        
        fps = RUNTIME_STATE["clock"].get_fps()
        RUNTIME_STATE["FPS"] = int(fps)
        pygame.display.flip()
        RUNTIME_STATE["clock"].tick(TARGET_FPS)
    pygame.quit()
    sys.exit()

main()


#Current issues:
#Enemies do not damage Ducky correctly


#LEVELS AND PROGRESS
#1 (MOSTLY DONE, NEED TO UPDATE SITTING DUCK AND MAYBE RE-VISE SPEECH)
#Speech 1-Mention moving forward automatically, space to break, turning like a boat. (DONE)
#Level 1-Tutorial for movement-Linear path, 1 enemy at the end (DONE)
#2
#Speech 2-Mention shooting to gain speed mult and move faster, but breaking will be less effective. Taking damage will lower or reset speed mult (DONE)
#Level 2-Tutorial for combo system, still only stationary enemies
#3
#Speech 3-Mention buffs that can raise your damage dealt and minimum speed mult.
#Level 3-Introduce chasing enemies. Lots of blocks to hide behind. 
#Enemy chaser:
#Collision works enough
#Kinda dumb but that's part of the appeal

#Speech 4-Mention that if Slick keeps up the good work, he can come aboard the train
#Level 4-Tons of chasing enemies. Maybe some stationary ones? Introduce the destrucable blocks as well. 

#Level 5-Introduce fish enemies

#Level 6 onward-???, swap to train local for later levels

#Final level-boss fight with Don Pigeon

#Why is the player killing all the birds?
#-To become capo
#Why does Don Pigeon want Slick killing all these enemy birds?
#-They're dispespecting the lake


#Player physics continuous tweaking:
#Still doesn't feel fun enough

#Bouncing:
#Tied to framerate, way too fast on lower framerate.
#Unsure if bounce affects both enemy and player correctly
#Bouncing should be squishier and less dramatic

#Gun fire
#Needs tied to animation
#Can't work on it until animation is ready

#Enemy Stationary:
#Fine tune range it shoots at
#Fix issues with rate of fire
#Should either be allowed x number of bullets or fire every x seconds



#Add enemy fish
#A bit different from idle enemy
#Underwater and unshootable if not close
#Pops up to shoot when close
#Stays up and idle while close
#Goes back down if far away




#Everything missing in the first three levels besides sound, in order:
#Title screen needs replaced
#Cafe background needs replaced
#Text box needs replaced
#Dialog likely needs re-written
#Level 1
#Sleeping/sitting duck needs replaced, maybe with that sleeping Walrus thing?
#Sleeping/sitting duck needs hit and/or death animation
#Hit stop on bullet hitting enemy or player needs implemented
#UI needs implemented
#Ducky turning white needs implemented (may be able to do this with a python script), also programmed
#Bonk 90 needs to be replaced with the actual bonk animation
#Pause screen with options, just needs to be text in that nice game over font on a darkened transparent background
#Game over screen needs a text image that is just text with the options Retry Level, Restart Game, or Exit Game to layer over the game over screen
#Pause screen needs properly programmed
#Ducky dying/game over needs properly programmed
#Pigeons need hit animation
#Pigeons need death animation
#Level Clear screen needs replaced with a nice looking Level Clear message. Does not need to be full screen of artwork