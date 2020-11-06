from datetime import timedelta
from flask import Flask, jsonify

from posts.sqlite_repo import SqlitePostsRepo
from tools.my_json_encoder import MyJSONEncoder
# from posts.repo import InMemoryPostsRepo
# from users.repo import InMemoryUsersRepo
from flask_jwt_simple import JWTManager
from users.sqlite_repo import SqliteUsersRepo

from flask_restful import Api


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.json_encoder = MyJSONEncoder
        self.user_repo = SqliteUsersRepo("./db/redditclone.db")
        # app.user_repo = InMemoryUsersRepo()
        # self.post_repo = InMemoryPostsRepo()
        self.post_repo = SqlitePostsRepo("./db/redditclone.db")
        self.config['JWT_SECRET_KEY'] = 'super-secret'
        self.config['JWT_EXPIRES'] = timedelta(hours=24)
        self.config['JWT_HEADER_NAME'] = 'authorization'
        self.config['JWT_IDENTITY_CLAIM'] = 'user'
        self.api = Api(self)
        self.jwt = JWTManager(self)


main_app = MyApp(__name__, static_folder="./../static")


@main_app.jwt.expired_token_loader
def my_expired_token_callback():
    err_json = {
        "message": "expired token"
    }
    return jsonify(err_json), 401


@main_app.jwt.invalid_token_loader
@main_app.jwt.unauthorized_loader
def my_inv_unauth_token_callback(why):
    err_json = {
        "message": why
    }
    return jsonify(err_json), 401
