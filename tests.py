import unittest

from party import app
from model import db, example_data, connect_to_db
from flask import session

class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):

        result = self.client.get("/")
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"123 Magic Unicorn Way", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertIn(b"123 Magic Unicorn Way", result.data)
        self.assertNotIn(b"Please RSVP", result.data)



class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'SECRETSECRETSECRET'

        #Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        #Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games_w_no_rsvp(self):
        
        result = self.client.get('/games', follow_redirects = True)
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"123 Magic Unicorn Way", result.data)

    def test_games_w_rsvp(self):
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True
        
            result = self.client.get('/games')

            self.assertIn(b'Catland', result.data)
            self.assertIn(b'Cute Kitty Cats', result.data)


if __name__ == "__main__":
    unittest.main()
