# Neural Network Guessing Game

Guess the weight values and try beat the CPU!
Python 3.8.5
numpy 1.19.4


```
NEURAL NET WEIGHT GUESSING GAME
SPACE TO PROGRESS, Q TO QUIT
INCREASE PLAYER WEIGHTS: 0.001: w e r   0.1: W E R
DECREASE PLAYER WEIGHTS: 0.001: s d f   -0.1: S D F

[0]     [1]     [1]     [0]
[0]     [1]     [0]     [1]
[1]     [1]     [1]     [1]
 \       |       |       /
  \______|_______|______/
     ________|________
    |                 |
    | CPU     PLAYER  |
    |                 |
    |  0.4056  3.0047 |
    |                 |
    |  0.5413 -0.0065 |
    |                 |
    | -0.7286 -1.5153 |
    |_________________|
   __________|__________
  /      |       |      \
 /       |       |       \
[0.000] [1.000] [1.000] [0.000] ...TARGET
 |       |       |       |
[0.299] [0.444] [0.325] [0.414] ...OUTPUT (CPU)
[-0.30] [0.556] [0.675] [-0.41] ...ERROR (CPU)
 |       |       |       |
[0.180] [0.815] [0.816] [0.179] ...OUTPUT (PLAYER)
[-0.18] [0.185] [0.184] [-0.18] ...ERROR (PLAYER)
 \       |       |       /
  \______|_______|______/
     ________|________
    |                 |
    | CPU     PLAYER  |
    | 0.12937 0.00242 |
    |  PLAYER LEADS!  |
    |_________________|
```
