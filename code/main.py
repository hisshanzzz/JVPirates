from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld
from menu import MainMenu
from options import OptionsMenu
from credits import CreditsMenu
from win import CongratulationsScreen
from game_over import GameOverScreen
from button import Button

class Game:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('JVPirates')
    self.clock = pygame.time.Clock()
    self.running = True
    self.import_assets()
    
    # Initialize states
    self.state = 'main_menu'
    self.paused = False
    
    self.main_menu = MainMenu(self.display_surface, self.font, self.start_game, self.show_options, self.show_credits, self.quit_game)
    self.options_menu = OptionsMenu(self.display_surface, self.font, self.back_to_main_menu)
    self.credits_menu = CreditsMenu(self.display_surface, self.font, self.back_to_main_menu)
    self.congratulations_screen = CongratulationsScreen(self.display_surface, self.font, self.back_to_main_menu)
    self.game_over_screen = GameOverScreen(self.display_surface, self.font, self.restart_game, self.back_to_main_menu)
    
    self.ui = UI(self.font, self.ui_frames)
    self.data = Data(self.ui)
    self.tmx_maps = {
      0: load_pygame(join('data', 'levels', '0.tmx')),
      1: load_pygame(join('data', 'levels', '1.tmx')),
      2: load_pygame(join('data', 'levels', '2.tmx')),
      3: load_pygame(join('data', 'levels', '3.tmx')),
      4: load_pygame(join('data', 'levels', '4.tmx')),
      5: load_pygame(join('data', 'levels', '5.tmx')),
      }
    self.tmx_overworld = load_pygame(join('data', 'overworld', 'overworld.tmx'))
    self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
    self.bg_music.play(-1)
    
    # Pause menu
    self.pause_menu_buttons = [
      Button("Continue Game", self.font, (400, 250), "white", "blue", self.resume_game),
      Button("Back to Main Menu", self.font, (400, 320), "white", "blue", self.back_to_main_menu),
      Button("Quit Game", self.font, (400, 390), "white", "blue", self.quit_game),
    ]
  
  def start_game(self):
        self.state = "gameplay"

  def show_options(self):
        self.state = "options"

  def show_credits(self):
        self.state = "credits"

  def show_congratulations(self):
        self.state = "congratulations"

  def back_to_main_menu(self):
        self.state = "main_menu"
        self.paused = False
        self.main_menu.reset()  # Reset menu to initial state

  def restart_game(self):
        self.data.reset()
        self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
        self.state = "gameplay"
        self.paused = False

  def quit_game(self):
        self.running = False
  
  def switch_stage(self, target, unlock = 0):
    if target == 'level':
      self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
    else: # overworld
      if unlock > 0:
        self.data.unlocked_level = unlock
      else:
        self.data.health -= 1
      self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
  
  def import_assets(self):
    self.level_frames = {
      'flag': import_folder('graphics', 'level', 'flag'),
      'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
      'floor_spike': import_folder('graphics', 'enemies', 'floor_spikes'),
      'palms': import_sub_folders('graphics', 'level', 'palms'),
      'candle': import_folder('graphics', 'level', 'candle'),
      'window': import_folder('graphics', 'level', 'window'),
      'big_chain': import_folder('graphics', 'level', 'big_chains'),
      'small_chain': import_folder('graphics', 'level', 'small_chains'),
      'candle_light': import_folder('graphics', 'level', 'candle light'),
      'player': import_sub_folders('graphics', 'player'),
      'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
      'saw_chain': import_image('graphics', 'enemies', 'saw','saw_chain'),
      'helicopter': import_folder('graphics', 'level', 'helicopter'),
      'boat': import_folder('graphics', 'objects', 'boat'),
      'spike': import_image('graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
      'spike_chain': import_image('graphics', 'enemies', 'spike_ball', 'spiked_chain'),
      'tooth': import_folder('graphics', 'enemies', 'tooth', 'run'),
      'shell': import_sub_folders('graphics', 'enemies', 'shell'),
      'perl': import_image('graphics', 'enemies', 'bullets', 'pearl'),
      'items': import_sub_folders('graphics', 'items'),
      'particle': import_folder('graphics', 'effects', 'particle'),
      'water_top': import_folder('graphics', 'level', 'water', 'top'),
			'water_body': import_image('graphics', 'level', 'water', 'body'),
      'bg_tiles': import_folder_dict('graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('graphics','level', 'clouds', 'small'),
			'cloud_large': import_image('graphics','level', 'clouds', 'large_cloud')
    } 
    self.font = pygame.font.Font(join('graphics', 'ui', 'runescape_uf.ttf'), 40)
    self.ui_frames = {
      'heart': import_folder('graphics', 'ui', 'heart'), 
			'coin':import_image('graphics', 'ui', 'coin') 
    }
    self.overworld_frames = {
      'palms': import_folder('graphics', 'overworld', 'palm'),
			'water': import_folder('graphics', 'overworld', 'water'),
			'path': import_folder_dict('graphics', 'overworld', 'path'),
			'icon': import_sub_folders('graphics', 'overworld', 'icon')
    }
    
    self.audio_files = {
      'coin': pygame.mixer.Sound(join('audio', 'coin.wav')),
			'attack': pygame.mixer.Sound(join('audio', 'attack.wav')),
			'jump': pygame.mixer.Sound(join('audio', 'jump.wav')), 
			'damage': pygame.mixer.Sound(join('audio', 'damage.wav')),
			'perl': pygame.mixer.Sound(join('audio', 'pearl.wav'))
    }
    self.bg_music = pygame.mixer.Sound(join('audio', 'Pirate 2.mp3'))
    self.bg_music.set_volume(1)
   
  def check_game_over(self):
     if self.data.health <= 0 and self.state != "game_over":
       self.state = "game_over"
       
  def resume_game(self):
    self.paused = False
    
  def pause_game(self):
    self.paused = True
    
  def run(self):
    while self.running:
      dt = self.clock.tick(60) / 1000

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        elif event.type == pygame.KEYDOWN and self.state == "gameplay":
          if event.key == pygame.K_p:
            self.paused = not self.paused

        if self.state == "main_menu":
          self.main_menu.update(event)
        elif self.state == "gameplay" and self.paused:
          for button in self.pause_menu_buttons:
            button.handle_event(event)
        elif self.state == "options":
          self.options_menu.update(event)
        elif self.state == "credits":
          self.credits_menu.update(event)
        elif self.state == "congratulations":
          self.congratulations_screen.update(event)
        elif self.state == "game_over":
          self.game_over_screen.update(event)

      if self.state == "main_menu":
        self.main_menu.draw()
      elif self.state == "gameplay":
        if self.paused:
          self.display_surface.fill("black")
          for button in self.pause_menu_buttons:
            button.draw(self.display_surface)
        else:
          self.current_stage.run(dt)
          self.ui.update(dt)
      elif self.state == "options":
        self.options_menu.draw()
      elif self.state == "credits":
        self.credits_menu.draw()
      elif self.state == "congratulations":
        self.congratulations_screen.draw()
      elif self.state == "game_over":
        self.game_over_screen.draw()

      if self.state == "gameplay":
        self.check_game_over()

      pygame.display.update()

  def tick(self):
    """Single frame — used by browser build."""
    if not self.running:
      return 0
    dt = self.clock.tick(60) / 1000

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN and self.state == "gameplay":
        if event.key == pygame.K_p:
          self.paused = not self.paused

      if self.state == "main_menu":
        self.main_menu.update(event)
      elif self.state == "gameplay" and self.paused:
        for button in self.pause_menu_buttons:
          button.handle_event(event)
      elif self.state == "options":
        self.options_menu.update(event)
      elif self.state == "credits":
        self.credits_menu.update(event)
      elif self.state == "congratulations":
        self.congratulations_screen.update(event)
      elif self.state == "game_over":
        self.game_over_screen.update(event)

    if self.state == "main_menu":
      self.main_menu.draw()
    elif self.state == "gameplay":
      if self.paused:
        self.display_surface.fill("black")
        for button in self.pause_menu_buttons:
          button.draw(self.display_surface)
      else:
        self.current_stage.run(dt)
        self.ui.update(dt)
    elif self.state == "options":
      self.options_menu.draw()
    elif self.state == "credits":
      self.credits_menu.draw()
    elif self.state == "congratulations":
      self.congratulations_screen.draw()
    elif self.state == "game_over":
      self.game_over_screen.draw()

    if self.state == "gameplay":
      self.check_game_over()

    pygame.display.update()
    return dt

if __name__ == '__main__':
  game = Game()
  game.run()