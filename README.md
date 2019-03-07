# A Simple Game of Hangman
## The Game
The game is a simple Python implementation of a Hangman game in roughly 100 LoC. 
* It records the amount of wins as the highscore.
* You can only guess a letter or number once.

### Web
Play the web-version by filling in 1 letter or number in the input box and clicking 'TRY!'

### API
Play the API version by appending the URL with ?api. You can send letters with both a querystring or POST variable `letter`. For example: `/?api&letter=a`. Once you win or lose, a new game is immediately ready to play.

## Install
### Flask
Run the game by exporting and setting `FLASK_APP` to main.py. Execute `flask run` and go to `http://127.0.0.1:5000/`.
### Heroku
The game is configured to run on Heroku. Simply deploy it to a dyno and enjoy. A demo runs here: https://damp-retreat-70644.herokuapp.com/

---

The code is formatted with [Black](https://github.com/ambv/black)
