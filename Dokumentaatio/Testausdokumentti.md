# Testing document

#### Dependency installations and running the test file

Because I am not using any package managers, you might need to download the dependacies required for testing. One is necessary for extraction of replay data and another 2 are for printing things in color in the command line.

The first one is (mpyq)[https://github.com/eagleflo/mpyq] so simply:
`pip install mpyq`

The second one is (termcolor)[https://pypi.org/project/termcolor/] so simply:
`pip install termcolor`

The third one is (colorama)[https://pypi.org/project/colorama/] so simply:
`pip install colorama`

#### What has been tested and how

Due to the nature of the project, I have opted out of unit testing. It is a bit of a shame, but when programming this kind of bot one usually runs the game everytime a potentially crashing change is made. This way once I ran into an error I could identify it easily and fix it. 

To some extent one can call running the game and looking for problems when things are happening in real time or going through the replays manually exploratory testing. This was done a lot.

The main and only testing is done on the replay files that are generated after every game is run. Through out this project I have generated a total of around 500 replays. 

For presenting the final test results I have used the replays of the latest version of the bot and latest patch in the actual of sc2. 

I have divided the test results by replay cataloging by opening strategy and race of default elite/veryhard bots. This is the hardest bot that does not cheat. Also the default bots even within the same difficulty have different strategies so it simulates wider range of playstyle. 

I opted out of testing pressure opener, because if I keep producing mass zergling behind it simply beats all default AIs except cheat insane regardless of the race. Also I ran out of time in the end. 

#### Empirical testing results

There are a total of 30 replays uploaded to the final submit. 

![screenshot of the above](https://github.com/rescawen/Wenlei-Dai-sc2bot-tiralabra/blob/master/Dokumentaatio/Screenshots/Screenshot%20(31).png)

Apparently sometimes opponents scout worker can bug out my build order resulting in a few losses in all 3 matchups and the reason why my versus Protoss was not 100%. There were some fundamental mistakes against Terran where a lot of games MyBot could have won but continously did a lot of unwise decisions to result in losses. Finally in the mirror matchup against Zerg, I simply played too greedy against many of the rushes that came my way. 

#### Runnable test program How can the tests be repeated

The main.py from tests folder is the program that one runs. However from command line it instantly runs and quits. So it doesn't run the result. Using visual studio code this was not a not a problem.
