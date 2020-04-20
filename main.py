import pygame
import random
import math
from pygame import mixer

#initialize the pygame 
pygame.init()

#create the screen,mode(width, height)
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('bg.jpg')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
PlayerX_change = 0
#PlayerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('alien.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(3)
	enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready" #you can't see the bullet on the screen
# Fire - The bullet is currently moving

#score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#to add more fonts download fonts from dafont.com put in folder and write the name on the line up

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
	score = font.render("Score : " + str(score_value),True, (255,0,0))
	screen.blit(score,(textX,textY))

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255,0,0))
	screen.blit(over_text,(200,250))

def player(x,y):
	screen.blit(playerImg, (x, y))#drawing image of player on the window

def enemy(x,y,i):
	screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
	global bullet_state # global - to access bullet_state within this function
	bullet_state = "fire"
	screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
	if distance < 27:
		return True
	else:
		return False

# Game Loop
running = True

while running:

	screen.fill((0, 0, 0))#fill RGB values(0 to 255)
	#background
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# If keystroke is pressed check whether it is left or right
		#KEYDOWN is pressing key and KEYUP is releasing key
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				PlayerX_change = -5
			if event.key == pygame.K_RIGHT:
				PlayerX_change = 5
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready": 
					bullet_Sound = mixer.Sound('laser.wav')
					bullet_Sound.play()
					# Get the current x coordinate of the spaceship
					bulletX = playerX
					fire_bullet(bulletX,bulletY)
			'''if event.key == pygame.K_UP:
				PlayerY_change == -0.3
			if event.key == pygame.K_DOWN:
				PlayerY_change == 0.3'''
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				PlayerX_change = 0

	
	playerX += PlayerX_change
	#playerY += PlayerY_change


	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736
	'''if playerY <= 100:
		playerY = 100
	elif playerY >=536:
		playerY = 536'''

	#enemy movement
	for i in range(num_of_enemies):

		#Game Over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i]

		if enemyX[i] <= 0:
			enemyX_change[i] = 3
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -3
			enemyY[i] += enemyY_change[i]

		#Collision
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			explosion_Sound = mixer.Sound('explosion.wav')
			explosion_Sound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)

		enemy(enemyX[i], enemyY[i],i)

	# Bullet movement
	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change

	


	player(playerX, playerY)
	show_score(textX, textY)
	pygame.display.update()#have to use it to update screen