# Bonuses

## Bonus: Use the whole hand

In the game so far, we have been using only the y position of the base of the middle finder to control the position of the paddle

In this bonus, we want to make the more fun and to actually use the whole hand as a pong racket. 
To do that, we would need to compute the collision between the hands and the ball. 
One way to do that is to consider a rectangular bounding box around the hand. 
The collision detection then just comes back to detecting rather if the ball touches a line of this bounding box. 



## Bonus+: Rock-Paper-Scissors using Hands (Training a ML model)

In this session, you saw how you could use MediaPipe to write a small pong game.
Although fun, it is not necessarily more natural to play pong with your hands compared with the keyboard.

In this bonus, I propose that you try to implement a rock-paper-scissors game to play against the computer using the hand-recognition.

To do that you will need several modules:

1. the game logic: here the idea can be to attribute different distributions for the computer to pick between rock, paper and scissors. You could for instance bias it towards rock and decide that 40\% of the times, the computer will play rock, 35\% for scissors and 25\% for paper.
2. classification between the three gestures. For that have a look at this link that will explain you how to use mediapipe to train a hand gesture classifier.
This tutorial can guide you in training a new gesture model with the three classes (rock, paper, Scissors) : https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/
Note that for that you will need to record some samples of the gestures
You will also need to install tensorflow to train the classification model.