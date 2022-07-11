from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage."""

        result = self.client.get("/")

        self.assertIn(b"The right place to chat", result.data)

    def test_movies_shows(self):
        """Test Movies & Shows page."""

        result = self.client.get("/media")

        self.assertIn(b"What are you looking for?", result.data)        



class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "teste2@teste.com", "password": "teste"},
                                  follow_redirects=True)
        self.assertIn(b"Hi, teste", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_comment_button(self):
        """Test that user can't comment when they're logged out."""

        result = self.client.get("/media/details/tt1099212")
        self.assertNotIn(b"Drop your comment here", result.data)
        self.assertIn(b"Log In to comment", result.data)

    def test_login_button(self):
        """Test that user can't log out when they're already logged out."""

        result = self.client.get("/")
        self.assertNotIn(b"Log Out", result.data)
        self.assertIn(b"Log In", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


if __name__ == "__main__":
    import unittest

    unittest.main()

