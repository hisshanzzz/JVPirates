from settings import *
from button import Button

class GameOverScreen:
  def __init__(self, screen, font, restart_callback, main_menu_callback):
    self.screen = screen
    self.font = font
    self.restart_game = restart_callback
    self.back_to_main = main_menu_callback

    self.buttons = [
      Button("Try Again", self.font, (400, 300), "white", "blue", self.restart_game),
      Button("Back to Main Menu", self.font, (400, 370), "white", "blue", self.back_to_main),
    ]

  def update(self, event):
    for button in self.buttons:
      button.handle_event(event)

  def draw(self):
    self.screen.fill("black")
    title_surface = self.font.render("Game Over", True, "red")
    self.screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 150))

    message_surface = self.font.render("You ran out of hearts.", True, "white")
    self.screen.blit(message_surface, (WINDOW_WIDTH // 2 - message_surface.get_width() // 2, 220))

    for button in self.buttons:
      button.draw(self.screen)
