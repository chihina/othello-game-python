# Othello-game-python
This is a othello game. It is written by python. 

## Environment
python3.7.1

And you can use requirements.txt
```
pip install -r requirements.txt
```

# How to Start game play
## 1. Command execution
You can only do below command.
```
python game.py 
```
After that, You can see below window.

![Top page](https://github.com/chihina/othello-game-python/blob/master/Images/top_resized.png)

## 2. Choice game mode
You can choice three game mode.
- Human vs Human
- Human vs CPU
- CPU vs CPU

## 3. Choice Order of hitting (Only Human vs CPU mode)
You can choice order of hitting for human.  
![Choice human_page](https://github.com/chihina/othello-game-python/blob/master/Images/human_choice_resized.png)

## 4. Choice CPU mode (If you play Human vs Human mode, this part is unrelated)
You can choice three CPU mode
- Weak: This CPU hit piece based on random number
- Little strong: This CPU hit piece base on random number and *rule*  ( *rule*: hit coorner cell prior to other pieces )
- strong: This CPU hit piece based on static evaluation value of cell  
![Choice cpu_page](https://github.com/chihina/othello-game-python/blob/master/Images/cpu_choice_resized.png)

If you finished 1-4 part, game will start!!

# How to play game
Click around cell you wanna hit.    
( You can hit the cell which is annotated by red circle. The circle shows cell whice you can hit. ) 

![Choice page](https://github.com/chihina/othello-game-python/blob/master/Images/choice_resized.png)
