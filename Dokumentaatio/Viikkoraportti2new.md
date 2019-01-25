## Week report 2

### What have I done this week?

### How has the project progressed?

### What did I learn this week?

### What problems did I encounter this week?

### What will I do next?

This week I have been refactoring my code and adding functionalities. Due to the nature of this project we are using asynchronous methods and everything is running under the method [_on_step in the BotAi class_](https://github.com/Dentosal/python-sc2/blob/master/sc2/bot_ai.py#L594).

When I was trying to get basic functionality working, it was just a long list of conditionals and loops under that method. I have now refactored so that most different tasks are have their method. Many of these methods have hard coded conditional logic on when to do what. For example algorithmicly speaking finding targets requires prioritization of what to fight, whether it be enemy units, enemy buildings or the spawning location of the opponent. Another example is how to use fly scouts in a basic pattern over the map to acquire information. With this information in turn we can make a better decision on how to use the army that we have built. 

The project has been progressing well without any integration hell problems. For example everytime I am running the game to see how my Bot behaves it creates a replay. This screen is an example of just how many trials have been going on. 
![screenshot](https://github.com/rescawen/Wenlei-Dai-sc2bot-tiralabra/blob/master/Dokumentaatio/Screenshots/Screenshot%20(17).png) 

I have learned about the programming concept of hooks. For example when a certain structure/unit/technology finishes it will automatically do something. In a game that is in real time, time itself becomes a resource and that is why we want to have the sequence in which we do things continueing at a rate as fast as possible. 

Thankfully there has not been integration hell problems. The problems that I encountered this week are very fundamental. There is a specific output/result I want my bot to accomplish and it simply requires a lot trial and error to tweak small things right. I have tried to import the project from GitLab to Github but it might run into some problems. 

I really want to continue to add functionality to improve my bots winning ability since the competition is entering its final weeks. In terms of testing, unit testing can possibly be done by playing a blank game without an opponent. During this blank game I would print certain statistics out to the console that reflect what is happening during the game. With these text prints I can do some kind of assert_equals to my expectations of what they should be. True unit testing is simply not possible because I am writing the bot in high level of abstraction. This means that I have no control on what happens once the game crashes due to a programming error.  
