# Secret Hitler Online Edition

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Secret Hitler Online Edition is a python script for people who want to play Secret Hitler even in the quarantine. You can now play the game over some video conferencing software such as Discord, Zoom, etc.

Disclaimer: I wrote this in a hurry, so the code is hideous. For the safety of your brain cells, it is recommended not to look at the code.

---
### Installation

Only one of the players (host) needs to run this software. Other players are only required to install [Telegram](https://telegram.org/) to their mobile devices.

This software requires [Python 3](https://www.python.org/downloads/) to run. First, install Python if you haven't already. 

Install the dependencies using pip using the terminal. For Anaconda installations, it is also possible to call pip from the IPython console. 

```sh
$ pip install -r requirements.txt
```

You'll need a telegram API token. Just talk to [BotFather](https://t.me/botfather) to create your telegram bot. After you got your token, create a txt file called `token.txt` and paste your token to the first line. Then paste your bot username to the second line. Your `token.txt` file should look like this:
```
12345678910:ABCDEFABCDEFABCDEFABCDEFABCDEFABCDEF
my_bot_name
```

Now we are all ready. To start the game, just run the python script `SecretHitler.py`

```sh
$ python SecretHitler.py
```

---
## Usage

#### Step 1

- **Host**

    First, gather players and share your screen. The script will ask you if you want to change players. Saying yes will start the lobby for the players to connect. Wait until all players (including host) to join.
    ```
    Do you want to change players? [Y/n]:y
    Please install Telegram and go to https://t.me/my_bot_name
    Press Enter once everybody joins.
    ```
- **Players**

    Go to https://t.me/my_bot_name, as seen on the host's screen. The bot will guide you to join. Here are the commands:
    * `/start`: Displays welcome message.
    * `/join`: Makes the player enter the game.

    Once someone joins, the host will show that person has connected.
    ```
    John has joined the game.
    ```
#### Step 2
- **Basic game play**
  
    Press enter to start the game. Once the game window opens, everyone will receive a message about their secret role. The fascists will also be informed of other fascists and Hitler. 

    In the game window, you'll see the player names on the left. To select someone president, click on their name once. The name will be highlighted yellow. Clicking again will select that person as chancellor and highlight green. Clicking one more time will deselect that person.

    After selecting the president and chancellor, click **Ja-Nein** image. This will start the voting process. After everyone votes, the results will be sent with the information on who voted what. If the president and chancellor lost the election, just redo the process above.
    
    If the president and chancellor win the election, click the drawable cards on the left. This will send the top three cards to the president. President selects one to discard, and the game sends the remaining two cards to the chancellor. When chancellor discards one card as well, the remaining card will be shown on the game screen. The process is the same for the rest of the game.
    
    When there are less than three cards to draw, click on the discarded cards to shuffle the deck.
    
- **Special actions**
    - **Election tracker**
        
        The election tracker is there just to mark the progress. Click on any spot to move the coin to the corresponding place. When the coin is at the final spot and hosts click to the first spot, the policy on top of the policy deck will be revealed and enacted.

    - **The president examines top three cards**
        
        If there are 5-6 players, the third fascist card has a special ability to make the president examine the top three cards. To invoke this ability, click on the third fascist card when the third fascist policy is enacted while the old president is selected.
    
    - **The president investigates a player's identity card**
        
        7-10 player games, there is a special ability to make the president see another player's identity card. To invoke this ability, keep the old president selected, highlight the person to be investigated green (same as selecting as chancellor) then click on the corresponding fascist card when that fascist policy is enacted. This will send the green highlighted person's fascist/liberal status to the old president. 
    
    - **Other actions**
        
        The other actions, such as selecting the next president or killing a player does not require the game's intervention. The host should deal with those actions himself/herself.
    
#### Step 3
- **Starting a new game or closing the game**
    
    There is no message when a side wins the game. Please stop playing when the game is over since otherwise, the game crashes, and when the game crashes, telegram bot may stay alive, which would make the game not open again unless the corresponding python process is killed.
There isn't a button to start a new game, either. Close the game screen and wait for the python process to end. **Don't close the _terminal window_ before the process ends.** Then you can just restart the game and say "no" when asked to change the players.



