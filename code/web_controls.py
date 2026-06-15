import pygame
import sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

WEB_MODE = sys.platform == 'emscripten'

# On-screen buttons for browser / touch play
BUTTONS = {
  'left': pygame.Rect(24, WINDOW_HEIGHT - 120, 72, 72),
  'right': pygame.Rect(120, WINDOW_HEIGHT - 120, 72, 72),
  'up': pygame.Rect(72, WINDOW_HEIGHT - 196, 72, 72),
  'down': pygame.Rect(72, WINDOW_HEIGHT - 44, 72, 72),
  'jump': pygame.Rect(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 120, 96, 72),
  'attack': pygame.Rect(WINDOW_WIDTH - 232, WINDOW_HEIGHT - 120, 96, 72),
  'enter': pygame.Rect(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 210, 96, 56),
}

KEY_MAP = {
  'left': pygame.K_LEFT,
  'right': pygame.K_RIGHT,
  'up': pygame.K_UP,
  'down': pygame.K_DOWN,
  'jump': pygame.K_SPACE,
  'attack': pygame.K_x,
  'enter': pygame.K_RETURN,
}

LABELS = {
  'left': '<',
  'right': '>',
  'up': '^',
  'down': 'v',
  'jump': 'JMP',
  'attack': 'ATK',
  'enter': 'GO',
}


class WebControls:
  def __init__(self, font):
    self.font = font
    self.active = set()
    self.pointer_buttons = {}
    self.enabled = WEB_MODE

  def handle_event(self, event):
    if not self.enabled:
      return

    if event.type == pygame.FINGERDOWN:
      self._press_at(event.x * WINDOW_WIDTH, event.y * WINDOW_HEIGHT, event.finger_id)
    elif event.type == pygame.FINGERUP:
      self._release(event.finger_id)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      self._press_at(*event.pos, 0)
    elif event.type == pygame.MOUSEBUTTONUP:
      self._release(0)

  def _press_at(self, x, y, pointer_id):
    for name, rect in BUTTONS.items():
      if rect.collidepoint(x, y):
        self.active.add(name)
        self.pointer_buttons[pointer_id] = name
        break

  def _release(self, pointer_id):
    name = self.pointer_buttons.pop(pointer_id, None)
    if name:
      self.active.discard(name)
      if self.enabled:
        key = KEY_MAP[name]
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key, unicode=''))

  def inject_keys(self):
    if not self.enabled:
      return
    pressed = pygame.key.get_pressed()
    for name in self.active:
      key = KEY_MAP[name]
      if not pressed[key]:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, unicode=''))

  def draw(self, surface):
    if not self.enabled:
      return
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for name, rect in BUTTONS.items():
      color = (40, 90, 160, 170) if name in self.active else (20, 40, 80, 140)
      pygame.draw.rect(overlay, color, rect, border_radius=10)
      pygame.draw.rect(overlay, (255, 255, 255, 90), rect, 2, border_radius=10)
      label = self.font.render(LABELS[name], True, 'white')
      overlay.blit(label, label.get_rect(center=rect.center))
    surface.blit(overlay, (0, 0))
