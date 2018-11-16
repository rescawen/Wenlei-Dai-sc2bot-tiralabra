## Week report 3

### What have I done this week?

### How has the project progressed?

### What did I learn this week?

### What problems did I encounter this week?

### What will I do next?

The focus this week is to create the simplest and most effective zerg bot. Even the newest and greatest bot that deepmind demoed this year at blizzcon has a lot of fuzziness. By fuzziness I mean this is a very smart and capable bot that takes things very easy. Just like many other bots it is focusing on the higher level strategy. 

For example using playing musical instrument. A metaphor could be used that the melody that is played is already decent, but the execution each "click" is still relatively weak.

My focus is exactly the opposite. To try to cut corners to make this bot feel like a decent level (top 10-15%) human player executing this build order.

There are a total of 10 built in difficulties of AI in this game.

Ranging from Very Easy, Easy, Medium, Hard, Harder, Very Hard, CheatVision, CheatMoney, CheatInsane.

The crispZerglingRush is capable of defeating the CheatMoney (level 9) of built in A.I. 

I did not write all the code from scratch but merely modified it from the zergrush.py AI that is in the examples from the library that I am using with numerous amounts of trial and error to get the details correct. 

This shows that a knowledgable player can use something very simple to defeat more complex bots that are not designed for winning but merely practice. 

Essentially I am just using a bunch of if and for logics to create this bot. It is making sure all the elements of the game happen in the right order.

There was the idea of generating replay.data from playing many games as a way to do testing, but I could not do that amount of "horizontal integration" type of work for this week unfortunately. Due to this I still lack any of kind of organizing things into folders in my project.

The level 10 CheatInsane AI seems to be theoretically impossible to beat with a simple strategy that I have come up this week, because literally has vision and money hacks combined. This means exploring other types of solutions. It might be when I try to create a more complex bot, it will become less competitive in terms of winning not end up achieving the goal of beating the hardest AI. 

In the online guide I will be starting part7, which introduces neural networks to create higher level decision making. 



