from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Spike, Item, ParticleEfffectSprite
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell, Perl

from random import uniform

class Level:
  def __init__(self, tmx_map, level_frames, audio_files, data, switch_stage):
    self.display_surface = pygame.display.get_surface()
    self.data = data
    self.switch_stage = switch_stage
    
    # level data
    self.level_width = tmx_map.width * TILE_SIZE
    self.level_bottom = tmx_map.height * TILE_SIZE
    tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
    self.level_unlock = tmx_level_properties['level_unlock']
    if tmx_level_properties['bg']:
      bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
    else:
      bg_tile = None
    
    # groups
    self.all_sprites = AllSprites(
      width = tmx_map.width, 
      height = tmx_map.height,
      bg_tile = bg_tile,
      top_limit = tmx_level_properties['top_limit'],
      clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
      horizon_line = tmx_level_properties['horizon_line'])
    self.collision_sprites = pygame.sprite.Group()
    self.semi_collision_sprites = pygame.sprite.Group()
    self.damage_sprites = pygame.sprite.Group()
    self.tooth_sprites = pygame.sprite.Group()
    self.shell_sprites = pygame.sprite.Group()
    self.perl_sprites = pygame.sprite.Group()
    self.item_sprites = pygame.sprite.Group()
    
    self.setup(tmx_map, level_frames, audio_files)
    
    # frames
    self.perl_surf = level_frames['perl']
    self.particle_frames = level_frames['particle']
    
    # sounds
    self.coin_sound = audio_files['coin']
    self.coin_sound.set_volume(0.4)
    self.damage_sound = audio_files['damage']
    self.damage_sound.set_volume(0.5)
    self.perl_sound = audio_files['perl']
    
  def setup(self, tmx_map, level_frames, audio_files):
    # tiles
    for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
      for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
        groups = [self.all_sprites]
        if layer == 'Terrain': groups.append(self.collision_sprites)
        if layer == 'Platforms': groups.append(self.semi_collision_sprites)
        match layer:
          case 'BG': z = Z_LAYERS['bg tiles']
          case 'FG': z = Z_LAYERS['bg tiles']
          case _: z = Z_LAYERS['main']
        Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups)
    
    # bg details
    for obj in tmx_map.get_layer_by_name('BG details'):
      if obj.name == 'static':
        Sprite((obj.x, obj.y), obj.image, self.all_sprites, Z_LAYERS['main'])
      else:
        AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['main'])
        if obj.name == 'candle':
          AnimatedSprite((obj.x, obj.y) + vector(-20,-20), level_frames['candle_light'], self.all_sprites, Z_LAYERS['main'])
    
    # objects
    for obj in tmx_map.get_layer_by_name('Objects'):
      if obj.name == 'player':
        self.player = Player(
          pos = (obj.x, obj.y), 
          groups = self.all_sprites, 
          collision_sprites = self.collision_sprites, 
          semi_collision_sprites = self.semi_collision_sprites,
          frames = level_frames['player'],
          data = self.data,
          attack_sound = audio_files['attack'],
          jump_sound = audio_files['jump'])
      else:
        if obj.name in ('barrel', 'crate'):
          Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites) )
        else:
          # frames
          frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
          if obj.name == 'floor_spike' and obj.properties['inverted']:
            frames = [pygame.transform.flip(frame, False, True) for frame in frames]
        
          # groups
          groups = [self.all_sprites]
          if obj.name in ('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
          if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)
          
          # z index
          z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']
          
          # animation speed
          animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1,1)
          
          AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
          
      if obj.name == 'flag':
          self.level_finish_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))
            
          
    # moving objects
    for obj in tmx_map.get_layer_by_name('Moving Objects'):
      if obj.name == 'spike':
        Spike(
          pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
          surf = level_frames['spike'],
          radius = obj.properties['radius'],
          speed = obj.properties['speed'],
          start_angle = obj.properties['start_angle'],
          end_angle = obj.properties['end_angle'],
          groups = (self.all_sprites, self.damage_sprites))
        for radius in range(0, obj.properties['radius'], 20):
          Spike(
          pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
          surf = level_frames['spike_chain'],
          radius = radius,
          speed = obj.properties['speed'],
          start_angle = obj.properties['start_angle'],
          end_angle = obj.properties['end_angle'],
          groups = self.all_sprites,
          z = Z_LAYERS['bg details'])
        
      else:
        frames = level_frames[obj.name]
        groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
        if obj.width > obj.height: # horizontal
          move_dir = 'x'
          star_pos = (obj.x, obj.y + obj.height / 2)
          end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
        else: # vertical
          move_dir = 'y'
          star_pos = (obj.x + obj.width / 2, obj.y)
          end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
        speed = obj.properties['speed']
        MovingSprite(frames, groups, star_pos, end_pos, move_dir, speed, obj.properties['flip'])
        
        # saw chain
        if obj.name == 'saw':
          if move_dir == 'x':
            y = star_pos[1] - level_frames['saw_chain'].get_height() / 2
            left, right = int(star_pos[0]), int(end_pos[0])
            for x in range(left, right, 20):
              Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
          else:
            x = star_pos[0] - level_frames['saw_chain'].get_width() / 2
            top, bottom = int(star_pos[1]), int(end_pos[1])
            for y in range(top, bottom, 20):
              Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
    
    # enemies
    for obj in tmx_map.get_layer_by_name('Enemies'):
      if obj.name == 'tooth':
        Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
      if obj.name == 'shell':
        Shell(
          pos = (obj.x, obj.y), 
          frames = level_frames['shell'], 
          groups = (self.all_sprites, self.collision_sprites, self.shell_sprites), 
          reverse = obj.properties['reverse'], 
          player = self.player, 
          create_perl = self.create_perl)
    
    # items
    for obj in tmx_map.get_layer_by_name('Items'):
      Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)
      
    # water
    for obj in tmx_map.get_layer_by_name('Water'):
      rows = int(obj.height / TILE_SIZE)
      cols = int(obj.width / TILE_SIZE)
      for row in range(rows):
        for col in range(cols):
          x = obj.x + col * TILE_SIZE
          y = obj.y + row * TILE_SIZE
          if row == 0:
            AnimatedSprite((x, y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
          else:
            Sprite((x, y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])
  
  def create_perl(self, pos, direction):
    Perl(pos, (self.all_sprites, self.damage_sprites, self.perl_sprites), self.perl_surf, direction, 150)
    self.perl_sound.play()
    
  def perl_collision(self):
    for sprite in self.collision_sprites:
      perl_sprite = pygame.sprite.spritecollide(sprite, self.perl_sprites, True)
      if perl_sprite:
        ParticleEfffectSprite((perl_sprite[0].rect.center), self.particle_frames, self.all_sprites)
  
  def hit_collision(self):
    for sprite in self.damage_sprites:
      if sprite.rect.colliderect(self.player.hitbox_rect):
        self.player.get_damage()
        self.damage_sound.play()
        if hasattr(sprite, 'perl'):
          sprite.kill()
          ParticleEfffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)
  
  def item_collision(self):
    if not self.item_sprites:
      return

    # Use hitbox + last position so fast movement doesn't skip pickups
    collect_rect = self.player.hitbox_rect.union(self.player.old_rect).inflate(50, 40)

    for item in list(self.item_sprites):
      if item.rect.colliderect(collect_rect):
        item.activate()
        ParticleEfffectSprite((item.rect.center), self.particle_frames, self.all_sprites)
        item.kill()
        self.coin_sound.play()
  
  def attack_collision(self):
    if not self.player.attacking:
      return

    attack_rect = self.player.rect.copy()
    reach = 90
    if self.player.facing_right:
      attack_rect.width += reach
    else:
      attack_rect.x -= reach
      attack_rect.width += reach
    attack_rect = attack_rect.inflate(10, 30)

    targets = (
      self.tooth_sprites.sprites() +
      self.shell_sprites.sprites() +
      self.perl_sprites.sprites()
    )
    for target in targets:
      if attack_rect.colliderect(target.rect):
        ParticleEfffectSprite((target.rect.center), self.particle_frames, self.all_sprites)
        target.kill()
        self.coin_sound.play()
  
  # making player camera movement(level display) constraints
  def check_constraints(self):
    # left right
    if self.player.hitbox_rect.left <= 0:
      self.player.hitbox_rect.left = 0
    if self.player.hitbox_rect.right >= self.level_width:
      self.player.hitbox_rect.right = self.level_width
      
    # bottom border
    if self.player.hitbox_rect.bottom > self.level_bottom:
      self.switch_stage('overworld', -1)
      
    # success
    if self.player.hitbox_rect.colliderect(self.level_finish_rect):
      self.switch_stage('overworld', self.level_unlock)
    
  def run(self, dt):
    self.display_surface.fill('black')
    
    self.all_sprites.update(dt)
    self.perl_collision()
    self.attack_collision()
    self.hit_collision()
    self.item_collision()
    self.check_constraints()
    
    self.all_sprites.draw(self.player.hitbox_rect.center, dt)
