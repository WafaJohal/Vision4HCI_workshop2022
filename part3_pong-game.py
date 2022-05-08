# Import
import pygame
import cv2
import numpy as np
import random
import mediapipe as mp
import sys
from pygame.locals import *


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

 
# Initialize
pygame.init()
 
# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My HandControlled Game")
 
# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()


# Game Globals
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
l_paddle_vel = 0
r_paddle_vel = 0
l_score = 0
r_score = 0
l_paddle_pos = [HALF_PAD_WIDTH - 1,height//2]
r_paddle_pos = [width +1 - HALF_PAD_WIDTH,height//2]


#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

 
# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
 

#keydown handler
def keydown(event):
    global l_paddle_vel, r_paddle_vel
    
    if event.key == K_UP:
        r_paddle_vel = -8
    elif event.key == K_DOWN:
        r_paddle_vel = 8
    elif event.key == K_w:
        l_paddle_vel = -8
    elif event.key == K_s:
        l_paddle_vel = 8

#keyup handler
def keyup(event):
    global l_paddle_vel, r_paddle_vel
    
    if event.key in (K_w, K_s):
        l_paddle_vel = 0
    elif event.key in (K_UP, K_DOWN):
        r_paddle_vel = 0


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [width//2,height//2]
    horz = random.randrange(5,15)
    vert = random.randrange(5,15)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]


# define event handlers
def init():
    l_paddle_pos = [HALF_PAD_WIDTH - 1,height//2]
    r_paddle_pos = [width +1 - HALF_PAD_WIDTH,height//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)





# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()


    # OpenCV
    success, img = cap.read()

    with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7) as hands:

        # Convert the BGR image to RGB, flip the image around y-axis for correct 
        # handedness output and process it with MediaPipe Hands.
        results = hands.process(cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1))

        # Print handedness (left v.s. right hand).
        print(results.multi_handedness)

        if not results.multi_hand_landmarks:
            continue

        # Draw hand landmarks of each hand.
        image_hight, image_width, _ = img.shape
        annotated_image = cv2.flip(img.copy(), 1)
        for hand_landmarks in results.multi_hand_landmarks:
            
            # Print index finger tip coordinates.
            print(
                f'Index finger MCP coordinate: (',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * image_width}, '
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_hight})'
            )

            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * image_width <= width // 2:
                l_paddle_pos[1] = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y *image_hight)
                print("updated" ,l_paddle_pos[1])
            elif hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x* image_width > width // 2:
                r_paddle_pos[1] = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y*image_hight)

            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())


    imgRGB = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))




 
    # Apply Logic
    pygame.draw.line(window, WHITE, [width // 2, 0],[width // 2, height], 1)
    pygame.draw.line(window, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, height], 1)
    pygame.draw.line(window, WHITE, [width - PAD_WIDTH, 0],[width - PAD_WIDTH, height], 1)
    pygame.draw.circle(window, WHITE, [width//2, height//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if l_paddle_pos[1] > HALF_PAD_HEIGHT and l_paddle_pos[1] < height - HALF_PAD_HEIGHT:
        l_paddle_pos[1] += l_paddle_vel
    elif l_paddle_pos[1] == HALF_PAD_HEIGHT and l_paddle_vel > 0:
        l_paddle_pos[1] += l_paddle_vel
    elif l_paddle_pos[1] == height - HALF_PAD_HEIGHT and l_paddle_vel < 0:
        l_paddle_pos[1] += l_paddle_vel
    
    if r_paddle_pos[1] > HALF_PAD_HEIGHT and r_paddle_pos[1] < height - HALF_PAD_HEIGHT:
        r_paddle_pos[1] += r_paddle_vel
    elif r_paddle_pos[1] == HALF_PAD_HEIGHT and r_paddle_vel > 0:
        r_paddle_pos[1] += r_paddle_vel
    elif r_paddle_pos[1] == height - HALF_PAD_HEIGHT and r_paddle_vel < 0:
        r_paddle_pos[1] += r_paddle_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])


   #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= height + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(l_paddle_pos[1] - HALF_PAD_HEIGHT,l_paddle_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= width + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(r_paddle_pos[1] - HALF_PAD_HEIGHT,r_paddle_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= width + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

  

    #draw paddles and ball
    pygame.draw.circle(window, RED, ball_pos, 20, 0)
    pygame.draw.polygon(window, GREEN, [[l_paddle_pos[0] - HALF_PAD_WIDTH, l_paddle_pos[1] - HALF_PAD_HEIGHT], [l_paddle_pos[0] - HALF_PAD_WIDTH, l_paddle_pos[1] + HALF_PAD_HEIGHT], [l_paddle_pos[0] + HALF_PAD_WIDTH, l_paddle_pos[1] + HALF_PAD_HEIGHT], [l_paddle_pos[0] + HALF_PAD_WIDTH, l_paddle_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(window, GREEN, [[r_paddle_pos[0] - HALF_PAD_WIDTH, r_paddle_pos[1] - HALF_PAD_HEIGHT], [r_paddle_pos[0] - HALF_PAD_WIDTH, r_paddle_pos[1] + HALF_PAD_HEIGHT], [r_paddle_pos[0] + HALF_PAD_WIDTH, r_paddle_pos[1] + HALF_PAD_HEIGHT], [r_paddle_pos[0] + HALF_PAD_WIDTH, r_paddle_pos[1] - HALF_PAD_HEIGHT]], 0)

 
 
    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    window.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    window.blit(label2, (width/2 +50, 20))  
    
 



    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)