Implementation document
Project structure
Implemented time and space complexities (big-O complexity analysis of (pseudo)code)
Comparative performance and complexity analysis if applicable
Possible flaws and improvements
Sources

I have decided to design the core of the logic for sequencing events based on time. This does operate on the assumption that my plan is not disturbed heavily in terms of battles going on before my bot is ready for them. In other words I am blindly building military units and workers at a certain sequence. 

So the logic many of times is looking at only the game state in terms what it should be doing OR a combination of time of the game plus the game state. 


