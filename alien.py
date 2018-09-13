import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self,ai_settings,screen):
		super(Alien,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#maybe its the origin point?
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		self.x = float(self.rect.x)		
	
		
	def check_edge(self):
		
		if self.rect.right >= self.screen.get_rect().right:
			return True
		if self.rect.left <= 0 :
			return True
		
	def update(self):
		self.rect.x += (self.ai_settings.alien_speed*self.ai_settings.alien_flip)

		
	def blitme(self):
		self.screen.blit(self.image,self.rect)
		
		
		
		