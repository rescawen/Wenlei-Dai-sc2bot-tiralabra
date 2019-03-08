# Implementation document

#### Project structure

![screenshot of rough structure](https://github.com/rescawen/Wenlei-Dai-sc2bot-tiralabra/blob/master/Dokumentaatio/Screenshots/IMG_0075.jpg)

I have decided to design the core of the logic for sequencing events based on time. This does operate on the assumption that my plan is not disturbed heavily in terms of battles going on before my bot is ready for them. In other words I am blindly building military units and workers at a certain sequence. 

#### Implemented time and space complexities

Most of the time when we go through any kind of list, it is iterating through all the units we have and issueing a command for them. The time complexity for that is O(n). In complex micro situations technically we can issue multiple loops for all the units but since we are not doing that at all here it does not apply. 

The only data structure used in this is the simple priority queue based on the list. Enqueuing and dequeuing should both take O(1) since I am using the index of a list as the priority of the queue. There are so many cool things that one potentially do with queues. 

Also it turns that is is impossible to analyse the time limit for calls in this game, because we don't know what the game itself is actually doing when executing on a call. For example what pathfinding or lists it is using are unknown.

#### Possible flaws and improvements

There is only one known game crashing bug at the moment. It is on [line 63](https://github.com/rescawen/Wenlei-Dai-sc2bot-tiralabra/blob/master/bot/main.py#L63) in the bot class for when the hatchery dies. Right now a few functions are dependent on that variable and when trying to fix the problems, I would break the functions so that they would stop properly.

Right now my bot is basically grouping units up and attack moving without micro management of the units. Good unit micro is fundamental to the playing the game and it is completely missing. That being said zerg is the race that relies least on micro and most on attack move. 

A framework for build orders would be really great. Right now they are all very manual and there are repetitive codes in earlyGameBuildOrder.

Reprioritization in the unit queue is key to giving the bot reactionary instructions. For when enemy is attacking one should immediately cease all non military production and focus completely on surviving.

#### Sources

https://pythonprogramming.net/starcraft-ii-ai-python-sc2-tutorial/

Big thanks to [Dentosal](https://github.com/Dentosal) who is the main developer for the python-sc2 library and [Blodir](https://github.com/Blodir) who is champion of the artificial overmind challenge. 



