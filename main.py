from flask import Flask, session, redirect, request, jsonify, render_template
from dataclasses import dataclass

import random
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

WORDS = ["3dhubs", "marvin", "print", "filament", "order", "layer"]


@dataclass
class Hangman:
    word: str = ""
    word_list: list = None
    word_obfuscate: list = None
    tried_chars: list = None
    tries: int = 5

    def new_game(self):
        """
        Start a new game of Hangman
        """
        self.word = random.choice(WORDS)
        self.word_list = [char for char in self.word]
        self.word_obfuscate = ["_" for char in self.word]
        self.tried_chars = []
        self.tries = 5
        return self.__dict__

    def guess(self, letter):
        """
        Checks if a letter is in the Hangman-word and tracks counter.
        """
        if self.valid(letter):
            letter = letter.lower()
            found = False
            for ix, char in enumerate(self.word_list):
                if letter == char:
                    found = True
                    self.word_obfuscate[ix] = letter  # Solve a letter
            if not found:
                if letter not in self.tried_chars:  # You can't guess a character twice
                    self.tries -= 1
            self.tried_chars.append(
                letter
            )  # Add the guessed character to 'tried' chars
        else:
            return False  # If a letter is invalid, don't do anything
        return self.__dict__

    def won(self):
        return self.word_list == self.word_obfuscate

    def lost(self):
        return self.tries == 0

    def api(self):
        """
        Return a simple object with the word and the amount of tries left
        """
        return {"word": " ".join(self.word_obfuscate), "tries_left": self.tries}

    @staticmethod
    def valid(letter):
        """
        Validates if the submitted letter is allowed
        Requirements:
            - Single letter or number
            - No special characters
        Returns:
            True or False
        """
        pattern = re.compile("^[a-zA-Z0-9]{1}$")
        return pattern.match(letter)


@app.route("/", methods=["GET", "POST"])
def instance():
    """
    Runs a hangman game instance for the browser. Progress is stored in a server-side session.
    """
    if "instance" not in session:
        instance = Hangman()
        session["instance"] = instance.new_game()
    if "highscore" not in session:
        session["highscore"] = 0

    game = Hangman(**session.get("instance"))
    letter = request.values.get("letter") or request.args.get("letter")
    if letter:
        game.guess(letter)
        if game.won():
            session["highscore"] += 1
        session["instance"] = game.__dict__

    if request.args.get("api") == "":
        instance = Hangman(**session.get("instance"))
        j = instance.api()
        j["highscore"] = session.get("highscore")
        if instance.won() or instance.lost():
            session["instance"] = instance.new_game()
        return jsonify(j)
    else:
        return render_template("index.html")


@app.route("/restart")
def restart():
    """
    The restart function removes the current game from the session and redirects to /.
    """
    try:
        session.pop("instance")
    except:
        pass
    return redirect("/")

if __name__ == '__main__':
    app.run()