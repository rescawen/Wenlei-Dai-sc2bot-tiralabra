# User guide

How is the program executed. 

After completing the installation of the game, python-sc2 library, moving the Maps folder the correct directory and cloning this repository. The full instructions are in the README.

Run the bot: `python3 run_locally.py`

How do different features work

My bot supports 2 different early game openers and a unified gameplan after the openers. There are three different ways the bot can interact with opponents. 

1. Playing against default built in bots in the actual game client.
2. Playing against default built in example bots given by python-sc2 library.
3. Playing against you the human!

One can set all of this in run_locally file by changing the opponents part in the run function.

What kind of input does the program support

There is no input to the bot once the game is running. All the "input" is technically the code, which gives the instructions to the bot. However you can play against the bot by yourself. 

Where can the executable be found and where can required files be found

The bot simply starts an instance of a sc2 game, when everything is properly installed. In the case options 2 and 3 where you have another example bot or a human it starts 2 instances of the game.

