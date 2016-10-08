my ghost in the shell

## setup

This bot does not use the bot-api, it connects to the irc-server. Yes, twitch is using good old irc. That makes it fairly easy to create a bot.

* creat an user account on twitch the bot should use (you probably dont want to use your account!).
* go to: http://www.twitchapps.com/tmi/ create and grab your oauth token
* edit the config.py according to your needs (the oauth token is your "password"!)
* start the bot with `python3 tBot.py`
* profit

## add a command

to add a command follow these steps:

* be **@timkalation** or **@bison_42**
* type **!add** then the new command (like **!hype**) and then the text you wanted to show

```
!add !lol rofl die katz
```

then you can type 
```
!lol
```

and the bot wil write to the chat:
```
rofl die katz
```

## kill the ghost

* be **@timkalation** or **@bison_42**
* type **!kill** in the chat
* ...
* profit!

## bet module

in german (sorry ^^)

create a bet  
```
!wetten !start nameOfTheBet
```

place a bet:  
```
!wetten !das victory
!wetten !das loose 
!wetten !das 1:3
```
 
stop accepting new bets  
```
!wetten !gilt nameOfTheBet
```

end the bet  
```
!wetten !stop nameOfTheBet
```

## match

The match-module is a simple list for things like "who plays against me first".

* `!match` adds your username to the match list
* `!matchlist` shows the current match list
* `!matchclear` be timkalation or bison, clears the current match list

## other commands

* `!silence` activate/deactivate ALL chats from the bot
