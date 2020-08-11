from datetime import datetime, timedelta
from app import app, db
from app.models import User, Post
import unittest


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config['DATABASE_URI'] = 'sqlite///'  # using an in-memory sqlite for tests
        db.create_all()   # this db function creates all the tables


    def tearDown(self):
        db.session.remove()
        db.drop_all()   # drops all table


    
    def test_password_hashing(self):
        u = User(username='Yugon')
        u.set_password('ding')
        self.assertFalse(u.check_password('thud'))
        self.assertTrue(u.check_password('ding'))


    def test_avatar(self):
        u = User(username='Yugon', email='yugon@example.com')
        self.assertEqual(u.avatar(128), ('http://gravatar.com/'
                                        '70ed2ba3f9711d2cf7f681c38bd69c65',
                                        '?d=identicon?s=128'))


    def test_follow(self):
        user1 = User(username='Yugon', email='yugon@example.com')
        user2 = User(username='Kwame atta', email='kwameatta_undisputed@example.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        # to test that first it is an empty list
        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user2.followed.all(), [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, 'Kwame atta')
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, 'Yugon')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)


    def test_follow_posts(self):
        # create four users
        user1 = User(username='Yugon', email='yugon@example.com')
        user2 = User(username='Kwame atta', email='kwameatta_undisputed@example.com')
        user3 = User(username='Marduk', email='mardukbabel@example.com' )
        user4 = User(username='Togbe Tsali', email='togbetsali@example.com')
        db.session.add_all([user1, user2, user3, user4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body='post from Yugon', author=user1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body='post from Kwame Atta', author=user2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body='post from Marduk', author=user3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body='post from Togbe Tsali', author=user4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        user1.follow(user2)  # yugon follows kwame atta
        user1.follow(user4)  # yugon follows marduk
        user2.follow(user3)  # kwame atta follows marduk
        user3.follow(user4)  # marduk follows togbe tsali
        db.session.commit()


        # check the followed posts of the users
        f1 = user1.followed_posts().all()
        f2 = user2.followed_posts().all()
        f3 = user3.followed_posts().all()
        f4 = user4.followed_posts().all()
        self.assertEqual(f1, [p1, p2, p4])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
        






