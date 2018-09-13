import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up =True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keyup_envents(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
				ship.moving_down = False


def check_events(ai_settings,screen,ship,bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()	
		
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		
		elif event.type == pygame.KEYUP:
			check_keyup_envents(event,ship)
			

		
def update_screen(ai_settings,screen,ship,aliens,bullets):
	
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	
	pygame.display.flip()
	
def update_bullets(bullets):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <=0:
			bullets.remove(bullet)
	
	#print len(bullets)

def get_number_aliens_x (ai_settings,alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y = (ai_settings.screen_height - (3*alien_height)-ship_height)
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien = Alien(ai_settings,screen)
	alien_height = alien.rect.height
	alien_width = alien.rect.width
	alien.rect.x = alien_width+2*alien_width*alien_number
	alien.rect.y = alien_height+2*alien_height*row_number
	aliens.add(alien)
	
def create_fleet(ai_settings,screen,ship,aliens):
	alien =Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	#print number_rows,number_aliens_x
		
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
			

#update the direction of aliens

#check edge:
 
def check_fleet_edge(ai_settings,aliens):
	for i in aliens.sprites():
		if i.check_edge():
			edge_todo(ai_settings,aliens)
			break


#first drop an change direction
def edge_todo(ai_settings,aliens):
	for i in aliens.sprites():
		i.rect.y += ai_settings.alien_drop
	ai_settings.alien_flip *= -1



			
def update_aliens (ai_settings,stats,screen,ship,bullets,aliens):
	check_fleet_edge(ai_settings,aliens)
	aliens.update()
	check_collison (ai_settings,screen,ship,bullets,aliens)
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)

	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
def check_collison (ai_settings,screen,ship,bullets,aliens):
	if len(aliens) == 0:
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	if stats.ships_left > 0:
		stats.ships_left -=1
		
		aliens.empty()
		bullets.empty()
		
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
		sleep(0.5)
	else:
		stats.game_active = False
	
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			break
	
	


			







		
			
			
