from flask import Flask, session, redirect, request, render_template

import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

WORDS = ["3dhubs", "marvin", "print", "filament", "order", "layer"]

class Hangman:
    def __init__(self):
        self.word = random.choice(WORDS)
        self.word_list = [char for char in self.word]
        self.word_obfuscate = ["_" for char in self.word]
        self.lost = False
        self.counter = 0

@app.route("/", methods=['GET', 'POST'])
def run():
    if 'current' not in session:
        session['current'] = Hangman().__dict__
    if 'highscore' not in session:
        session['highscore'] = 0
        
    game = session.get("current")

    if request.method == 'POST' or request.args.get('letter') is not None:
        letter = request.values.get('letter') or request.args.get('letter')
        if len(letter) > 0:
            success = False
            letter = letter.lower()
            
            for ix, char in enumerate(game["word_list"]):
                if letter == char:
                    success = True
                    game["word_obfuscate"][ix] = letter
            
            if game["word_list"] == game["word_obfuscate"]:
                session["highscore"] += 1

            if not success:
                game["counter"] += 1
                if game["counter"] == 5:
                    game["lost"] = True
            
            session['game'] = game
    
    return render_template("index.html")

@app.route("/restart")
def restart():
    '''
    The restart function removes the current game from the session and redirects to /.
    '''
    session.pop("current")
    return redirect("/")
