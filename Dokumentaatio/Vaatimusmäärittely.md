# Design document

In Starcraft2 there are distinct 3 races. The race that I play with is Zerg and that will be where I focus on my efforts. There are a total of 6
unique matchups in the game, but from a subjective perspective one only needs to worry about 3 match ups. 

Starcraft2 offers a wide variety of maps, but the focus for this bot is to use standard competitive 1v1 maps. 

I will be using the follow guide made my sentdex [python sc2 tutorial](https://pythonprogramming.net/starcraft-ii-ai-python-sc2-tutorial/) 
as an anchor and direction of my focus. 

One can approach this project from a computer science or game objective perspective. One can create something that is very complex in terms of code but isn't very winning. One can go in the opposite direction of creating as simple as possible bot with least amount of lines of code to achieve a relatively high winrate. 

The goal of this project is to find a middleground. Where the winning capability and my personal learning process of this course are taken into account. 

Deep learning is the pipedream of this project, it was explained in the tutorial but as of now I have not been able to make it work on my own computer. It involves training a model based a very large amount of games and then using the model for the bot to make smarter decisions.

Due to the nature of this project, I won't be using any data structures or algorithms for anything very specific like in the exercises of [algorithm in problem solving](https://www.cses.fi/alon19/list). However from a high level strategic point of view it is similar to [minimax algorithm](https://materiaalit.github.io/intro-to-ai-18/part2/), where the bot is trying to cut off as many game tree possibilities to make it so that it's own logic will not be broken by entering an unknown situation. 

As of this time I am unsure whether my own code will affect time and space complexity. This is because I am using a library that is already created and my guess is that the time and space complexity are bound to how 



