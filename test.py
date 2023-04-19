from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_home(self):
        """Make sure HTML is displayed and session information is present."""
        with self.client:
            response = self.client.get("/")
            decoded = response.data.decode()
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numplays'))
            self.assertIn('<p>High Score:', decoded)
            self.assertIn('Score:', decoded)
            self.assertIn('<p>Games Played:', decoded)

    def test_valid_word(self):
        """Test if word is valid."""
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["P", "U", "P", "P", "Y"],
                                    ["P", "U", "P", "P", "Y"],
                                    ["P", "U", "P", "P", "Y"],
                                    ["P", "U", "P", "P", "Y"],
                                    ["P", "U", "P", "P", "Y"],]
        response = self.client.get('/check-word?word=puppy')
        self.assertEqual(response.json['response'], 'ok')

    def test_invalid_word(self):
        """Test if word not on board is in the dictionary."""
        self.client.get("/")
        response = self.client.get('/check-word?word=turkey')
        self.assertEqual(response.json['response'], 'not-on-board')

    def test_non_word(self):
        """Test if gibberish returns as 'not-word'."""
        self.client.get("/")
        response = self.client.get('/check-word?word=lsssdsjhoin')
        self.assertEqual(response.json['response'], 'not-word')

