#!env/Scripts/python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-21 23:56
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

import os.path
from datetime import datetime, timedelta
from unittest import TestCase, main

from app import app, db
from app.models import User, Post


class TestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + \
            os.path.join(app.config['BASE_DIR'], 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        user = User(nickname='LeiYue', email='mr.leiyue@gmail.com')
        avatar = user.avatar(128)
        expected = 'http://www.gravatar.com/avatar/75dbac863b02ff90d9ca7ed98da78026'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        user1 = User(nickname='leiyue', email='mr.leiyue@gmail.com')
        db.session.add(user1)
        db.session.commit()
        nickname1 = User.make_unique_nickname('leiyue')
        assert nickname1 != 'leiyue'
        user2 = User(nickname=nickname1, email='d0nny@163.com')
        db.session.add(user2)
        db.session.commit()
        nickname2 = User.make_unique_nickname('leiyue')
        assert nickname2 != 'leiyue'
        assert nickname2 != nickname1

    def test_follow(self):
        user1 = User(nickname='leiyue', email='mr.leiyue@gmail.com')
        user2 = User(nickname='d0nny', email='d0nny@163.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        assert user1.unfollow(user2) is None
        u = user1.follow(user2)
        db.session.add(u)
        db.session.commit()
        assert user1.follow(user2) is None
        assert user1.is_following(user2)
        assert user1.followed.count() == 1
        assert user1.followed.first().nickname == 'd0nny'
        assert user2.followers.count() == 1
        assert user2.followers.first().nickname == 'leiyue'
        u = user1.unfollow(user2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not user1.is_following(user2)
        assert user1.followed.count() == 0
        assert user2.followers.count() == 0

    def test_follow_posts(self):
        user1 = User(nickname='john', email='john@example.com')
        user2 = User(nickname='susan', email='susan@example.com')
        user3 = User(nickname='mary', email='mary@example.com')
        user4 = User(nickname='david', email='david@example.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)

        utc_now = datetime.utcnow()
        post1 = Post(body="post from john", author=user1, timestamp=utc_now + timedelta(seconds=1))
        post2 = Post(body="post from susan", author=user2, timestamp=utc_now + timedelta(seconds=2))
        post3 = Post(body="post from mary", author=user3, timestamp=utc_now + timedelta(seconds=3))
        post4 = Post(body="post from david", author=user4, timestamp=utc_now + timedelta(seconds=4))
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(post4)
        db.session.commit()

        user1.follow(user1)  # john follows himself
        user1.follow(user2)  # john follows susan
        user1.follow(user4)  # john follows david
        user2.follow(user2)  # susan follows herself
        user2.follow(user3)  # susan follows mary
        user3.follow(user3)  # mary follows herself
        user3.follow(user4)  # mary follows david
        user4.follow(user4)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.commit()

        f1 = user1.followed_posts().all()
        f2 = user2.followed_posts().all()
        f3 = user3.followed_posts().all()
        f4 = user4.followed_posts().all()
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [post4, post2, post1]
        assert f2 == [post3, post2]
        assert f3 == [post4, post3]
        assert f4 == [post4]

if __name__ == '__main__':
    main()
