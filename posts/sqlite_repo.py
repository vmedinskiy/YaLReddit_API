import datetime
from tools.misc import get_connection_cursor
from . import post


class SqlitePostsRepo(post.PostRepo):
    def __init__(self, name):
        self.name = name

    def elem_to_post(self, elem):
        post_dct = dict(
            zip(("id", "author_id", "author_name", "category", "score", "text", "title",
                 "type", "upvotePercentage", "views", "url", "created"), elem))
        post_dct["author"] = {"id": post_dct["author_id"], "username": post_dct["author_name"]}
        del post_dct["author_id"]
        del post_dct["author_name"]
        return post.Post(**post_dct)

    def get_all(self):
        query = """SELECT P.id,
       P.author   as author_id,
       U.username as author_name,
       P.category,
       P.score,
       P.text,
       P.title,
       P.type,
       P.upvotePercentage,
       P.views,
       P.url, P.created
    FROM posts P
         LEFT JOIN users U on P.author = U.id order by P.created DESC"""
        con, cur = get_connection_cursor(self.name)
        results = cur.execute(query).fetchall()
        res = list()
        for elem in results:
            res.append(self.elem_to_post(elem))
        con.close()
        return res

    def get_by_id(self, id):
        query = """SELECT P.id,
       P.author   as author_id,
       U.username as author_name,
       P.category,
       P.score, 
       P.text,
       P.title,
       P.type,
       P.upvotePercentage,
       P.views,
       P.url, P.created
    FROM posts P
         LEFT JOIN users U on P.author = U.id
                            WHERE P.id = ? order by P.created DESC"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (id,)).fetchone()
        if result is None:
            con.close()
            return None
        con.close()
        return self.elem_to_post(result)

    def get_by_user_login(self, login):
        query = """SELECT P.id,
               P.author   as author_id,
               U.username as author_name,
               P.category,
               P.score,
               P.text,
               P.title,
               P.type,
               P.upvotePercentage,
               P.views,
               P.url, P.created
            FROM posts P
                 LEFT JOIN users U on P.author = U.id
                 WHERE author_name= ? order by P.created DESC"""
        con, cur = get_connection_cursor(self.name)
        results = cur.execute(query, (login,)).fetchall()
        res = list()
        for elem in results:
            res.append(self.elem_to_post(elem))
        con.close()
        return res

    def get_by_category(self, cat):
        query = """SELECT P.id,
                       P.author   as author_id,
                       U.username as author_name,
                       P.category,
                       P.score,
                       P.text,
                       P.title,
                       P.type,
                       P.upvotePercentage,
                       P.views,
                       P.url, P.created
                    FROM posts P
                         LEFT JOIN users U on P.author = U.id
                         WHERE P.category= ? order by P.created DESC"""
        con, cur = get_connection_cursor(self.name)
        results = cur.execute(query, (cat,)).fetchall()
        res = list()
        for elem in results:
            res.append(self.elem_to_post(elem))
        con.close()
        return res

    def request_create(self, p):
        p.created = datetime.datetime.now()
        query = """INSERT INTO posts(author, created, category, score, text, title, type, upvotePercentage, views, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
        con, cur = get_connection_cursor(self.name)
        params = p.author.id, p.created, p.category, p.score, p.text, p.title, p.type, p.upvotePercentage, \
                 p.views, p.url
        result = cur.execute(query, params)
        if not result.rowcount > 0:
            con.close()
            return None
        p.id = result.lastrowid
        con.commit()
        con.close()
        return p

    def request_update(self, post):
        return

    def request_delete(self, id, user):
        p = self.get_by_id(id)
        if not p:
            return f"post does not exist for id: {id}"
        if p.author.id != user.id:
            return f"you are not author of this post id: {id}"
        del self.by_id[id]
        return None
