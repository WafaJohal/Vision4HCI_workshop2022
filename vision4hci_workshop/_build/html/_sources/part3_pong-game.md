# Part 3 The Hand-Controlled Pong Game

In this part, we will see how to setup the pong game and how to integrate the hand controller. 

## 3.1 Pong Game Explained

The game of pong is fairly basic. We have a ball, bouncing on the top and bottom part of our game arena. When the ball bounces on a paddle (placed on the left and right side of the arena) it is saved, if the ball passes through and touches the left of right side of the arena, a point is given to the player at the opposite side. 

## 3.2 PyGame Basics

Pygame is a python library that allow to easily create games. It has building functions to draw elements and manage events (such as key events0 that could be used to control our game. 
But for us it will be mainly used to setup the graphics and to handle the frame rate. 

You can already open the documentations of pygame and see the different functions to draw the elements of our game. 
https://www.pygame.org/docs/ref/draw.html


## 3.3 Setting-up the Game

We provide to you the skeleton of code for a game using pygame. 

```python
import pygame


# Initialize
pygame.init()
 
# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Hand Controlled Game")
 
# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()


# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

	# Game Logics….


    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)
```

Run the code and observe. 


## 3.4 Draw the paddles and the ball

The Paddles
Using the rect function of pygame, draw the left and right paddles

```python
PAD_WIDTH = 8
PAD_HEIGHT = 80
```
Draw the ball using the circle function

## 3.5 Game physics

```python
# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
		#########
		## Capture the index position 


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
    
    #ball collison check on gutters or paddles  == check for the left paddle
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(l_paddle_pos[1] - HALF_PAD_HEIGHT,l_paddle_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
       ##### WRITE the code for the right paddle

    #draw paddles and ball
   # …. 

 
 
    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    window.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    window.blit(label2, (width/2 +50, 20))  

```

## 3.6 Convert CV image into canvas

Now that you have the game setup, you will need to add you code to stream the video using opencv (as per section 1.3 and use mediapipe to obtain the position of the base of the index (this is the join we use to control the paddle).
The code below show you how to convert an opencv image into a surface array that can be use as a background of our game.

```python
imgRGB = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
imgRGB = np.rot90(imgRGB)
frame = pygame.surfarray.make_surface(imgRGB).convert()
frame = pygame.transform.flip(frame, True, False)
window.blit(frame, (0, 0))
```

```{note}
Note that you will need to capture the position of two hands, you can easily associate the control of the left and right paddle by using the x-position of the hand on the image. (i.e. if x<width/2 => control of the left paddle, else => control of the right paddle)
```
