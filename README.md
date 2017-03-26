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

## del a command

to remove a command follow these steps:

* be **@timkalation** or **@bison_42**
* type **!del** then the new command (like **!hype**)

```
!!del !lol
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

## greeting

The bot can greet users, add OR change a greeting text with:
```
!addGreeting merover * everyone is a hamster!
```

1. `!addGreeting` adds OR changes a greeting
2. Parameter: the Username (ALWAYS lowercase without @ !)
3. Parameter: a simple command that triggers the greeting
  * use * for the default greeting detection
  * CANT have spaces
  * MUST be one word
  * IS case sensitive!
4. Parameter: the greeting text

## submaster

add/remove sub masters  
WARNING: case sensitive!

* `!!submaster list` shows all sub masters
* `!!submaster add someTwitchUser` adds someTwitchUser as new sub master
* `!!submaster remove someTwitchUser` removes someTwitchUser as sub masters


## other commands

* `!silence` activate/deactivate ALL chats from the bot
* `!takebluepill`, `!bluepill` kills the short time memory / resets all timers for chat and interval messages
