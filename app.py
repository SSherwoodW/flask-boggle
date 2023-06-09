from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "sneaky-sneaky"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



boggle_game = Boggle()

@app.route("/")
def show_boggle():
    """show board."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get('numplays', 0)
    return render_template("index.html", board=board, highscore=highscore, numplays=numplays)

@app.route("/check-word", methods=["GET"])
def check_word():
    """Check if word is in the dictionary."""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({"response": response})

@app.route("/end-game", methods=["POST"])
def end_game():
    """Update high score if new score is greater than, & update numplays."""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    session["highscore"] = max(score, highscore)
    session["numplays"] = numplays + 1
    return 'game over'