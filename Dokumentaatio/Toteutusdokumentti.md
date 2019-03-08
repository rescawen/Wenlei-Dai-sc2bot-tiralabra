# Implementation document

#### Project structure

![screenshot of rough structure](https://github.com/rescawen/Wenlei-Dai-sc2bot-tiralabra/blob/master/Dokumentaatio/Screenshots/IMG_0075.jpg)

I have decided to design the core of the logic for sequencing events based on time. This does operate on the assumption that my plan is not disturbed heavily in terms of battles going on before my bot is ready for them. In other words I am blindly building military units and workers at a certain sequence. 

#### Implemented time and space complexities

The only data structure used in this is the simple priority queue based on the list. Enqueuing and dequeuing should both take O(1) since I am using the index of a list as the priority of the queue. There are so many cool things that one potentially do with queues. 

So the logic many of times is looking at only the game state in terms what it should be doing OR a combination of time of the game plus the game state. 

#### Possible flaws and improvements

There is only one known game crashing bug at the moment. It is on line XX in the bot class. Right now a few functions are dependent on that variable. 

Right now my bot is basically grouping units up and attack moving without micro management of the units. Good unit micro is fundamental to the playing the game and it is completely missing. That being said zerg is the race that relies least on micro and most on attack move. 

A framework for build orders would be really great. Right now they are all very manual and there are repetitive codes in earlyGameBuildOrder.

Reprioritization is key to giving the bot reactionary instructions. For example mineral/gas ratio thing..

#### Sources

https://pythonprogramming.net/starcraft-ii-ai-python-sc2-tutorial/

Big thanks to https://github.com/Dentosal, https://github.com/Blodir and spudde for giving advice which were key to writing a lot of the lines of the code. 



