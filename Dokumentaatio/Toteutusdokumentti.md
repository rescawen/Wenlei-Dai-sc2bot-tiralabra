Implementation document
Project structure
Implemented time and space complexities (big-O complexity analysis of (pseudo)code)
Comparative performance and complexity analysis if applicable
Possible flaws and improvements
Sources



I have decided to design the core of the logic for sequencing events based on time. This does operate on the assumption that my plan is not disturbed heavily in terms of battles going on before my bot is ready for them. In other words I am blindly building military units and workers at a certain sequence. 

So the logic many of times is looking at only the game state in terms what it should be doing OR a combination of time of the game plus the game state. 

There is only one known game crashing bug at the moment. It is on line XX in the bot class. Right now a few functions are dependent on that variable. 

Right now my bot is basically grouping units up and attack moving without micro management of the units. Good unit micro is fundamental to the playing the game and it is completely missing. That being said zerg is the race that relies least on micro and most on attack move. 

A framework for build orders would be really great. Right now they are all very manual and there are repetitive codes in earlyGameBuildOrder.

The only data structure used in this is the simple priority queue based on the list. Enqueuing and dequeuing should both take O(1) since I am using the index of a list as the priority of the queue. There are so many cool things that one potentially do with queues. 

Reprioritization is key to giving the bot reactionary instructions. For example mineral/gas ratio thing..
