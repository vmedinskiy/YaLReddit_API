from waitress import serve
from api.posts import PostListRes, PostRes
from api.users import RegisterRes, LoginRes, UserPosts
from app.app import main_app
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)


@main_app.route('/', defaults={'path': ''})
@main_app.route('/a/<path:path>')
@main_app.route('/u/<path:path>')
def root(path):
    return main_app.send_static_file("index.html")


main_app.api.add_resource(RegisterRes, '/api/register')
main_app.api.add_resource(LoginRes, '/api/login')
main_app.api.add_resource(PostListRes, '/api/posts/<category_name>', '/api/posts', '/api/posts/')
main_app.api.add_resource(PostRes, '/api/post/<int:post_id>')
main_app.api.add_resource(UserPosts, "/api/user/<user_login>")

if __name__ == '__main__':
    # main_app.run(host="0.0.0.0", port=8000)
    serve(main_app, host="0.0.0.0", port=8000)
