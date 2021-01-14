import os
import pygame
import random
import math

pygame.font.init()
pygame.display.set_caption("Acceleration Ball")

SCORE_FONT = pygame.font.SysFont("garamond", 30)
MENU_FONT = pygame.font.SysFont("times new roman", 20)

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BASE_VEL = 15
BALL_VEL = 4


WHITE = (255,255,255)
BLACK = (0,0,0)
BALL_WIDTH, BALL_HEIGHT = 22, 20
BAR_WIDTH, BAR_HEIGHT = 150, 20

BALL = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "ball.png")), (BALL_WIDTH, BALL_HEIGHT))
BAR = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bar.png")), (BAR_WIDTH, BAR_HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")), (WIDTH, HEIGHT))
WINNER_SCREEN = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "winner.png")), (WIDTH, HEIGHT))
MENU = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "menu.png")), (WIDTH, HEIGHT))

def main_menu():
    WIN.blit(MENU, (0,0))
    option1 = MENU_FONT.render("Press 'SPACE' to play",1,BLACK)
    option2 = MENU_FONT.render("Press 'F' to quit",1,BLACK)
    WIN.blit(option1, (WIDTH/2 - option1.get_width()/2, 600))
    WIN.blit(option2, (WIDTH/2 - option2.get_width()/2, 640))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_SPACE]:
            game_loop()
        elif key_pressed[pygame.K_f]:
            quit()
            pygame.quit()

def create_display(bar1, ball, score, speed):
    WIN.blit(BACKGROUND, (0,0))
    score = SCORE_FONT.render("Score: {}".format(score), 1, BLACK)
    net_speed = SCORE_FONT.render("Net Speed: {:.2f}".format(speed),1,BLACK)
    WIN.blit(score, (WIDTH/2 - score.get_width()/2, 20))
    WIN.blit(net_speed, (WIDTH/2 - net_speed.get_width()/2, 60))
    WIN.blit(BAR, (bar1.x,bar1.y))
    WIN.blit(BALL, (ball.x, ball.y))
    pygame.display.update()   

def manage_movement(bar1):  
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_RIGHT] and (bar1.x + BAR_WIDTH) <= WIDTH:
        bar1.x += BASE_VEL
    if key_pressed[pygame.K_LEFT] and (bar1.x) >= 0:
        bar1.x -= BASE_VEL

def ball_movement(ball, x_distance, y_distance):
    ball.x += x_distance
    ball.y += y_distance

def starting_movement():
    angles = [math.radians(60), math.radians(120), math.radians(150), math.radians(210), math.radians(330)]
    angle = random.choice(angles)
    x_distance = math.cos(angle) * BALL_VEL
    y_distance = math.sin(angle) * BALL_VEL
    return x_distance, y_distance

def changing_movement(ball, bar, score, x_distance, y_distance):
    if ball.x + x_distance < (0) or (ball.x + BALL_WIDTH + x_distance) > (WIDTH):
        x_distance *= -1
    if ball.y + y_distance < (0):
        y_distance *= -1
    if (ball.x >= bar.x) and ((ball.x) <= (bar.x + BAR_WIDTH)) and ((ball.y + BALL_HEIGHT/2) >= bar.y) and ((ball.y + BALL_HEIGHT/2) <= bar.y + BALL_HEIGHT):
        y_distance *= (-1 * math.sqrt(1.5))
        x_distance *= (math.sqrt(1.5))
        score += 1

    speed = math.sqrt(x_distance ** 2 + y_distance ** 2)

    return x_distance, y_distance, score, speed

def lose_condition(ball):

    if (ball.y + BALL_HEIGHT) > HEIGHT:
        return True

def end_screen(score,speed):

    WIN.blit(WINNER_SCREEN, (0,0))
    score_screen = SCORE_FONT.render("Score: {}".format(score), 1, BLACK)
    speed_screen = SCORE_FONT.render("Highest Net Speed: {:.2f}".format(speed),1,BLACK)
    options = MENU_FONT.render("Press 'SPACE' to play again, 'F' to quit.", 1, BLACK)
    WIN.blit(score_screen, (WIDTH/2 - score_screen.get_width()/2, 650))
    WIN.blit(speed_screen, (WIDTH/2 - speed_screen.get_width()/2, 700))
    WIN.blit(options, (WIDTH/2 - options.get_width()/2 , 750))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_SPACE]:
            game_loop()
        elif key_pressed[pygame.K_f]:
            run = False
            pygame.quit()
        
def game_loop():
    run = True
    clock = pygame.time.Clock()

    score = 0
    net_speed = BALL_VEL
    ball = pygame.Rect(WIDTH/2 - BALL_WIDTH/2, HEIGHT/2-BALL_HEIGHT/2, BALL_WIDTH, BALL_HEIGHT)
    bar1 = pygame.Rect(WIDTH/2 - BAR_WIDTH/2, HEIGHT - BAR_HEIGHT, BAR_WIDTH, BAR_HEIGHT)
    x_distance, y_distance = starting_movement()
 
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
         
        create_display(bar1,ball,score,net_speed)
        manage_movement(bar1)
        ball_movement(ball, x_distance, y_distance)
        x_distance, y_distance, score, net_speed = changing_movement(ball, bar1, score, x_distance, y_distance)

        if lose_condition(ball):
            break
    
    end_screen(score, net_speed)
    
    pygame.quit()

    

# This method starts the entire game
main_menu()