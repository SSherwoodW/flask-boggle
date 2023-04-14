from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "sneaky-sneaky"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



boggle_game = Boggle()

@app.route("/", methods=["GET", "POST"])
def show_boggle():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template("index.html", board=board)

@app.route("/check-word", methods=["POST"])
def check_word():
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({"response": response})