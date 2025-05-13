from py2neo import Graph, Node, Relationship
from datetime import datetime

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.utcnow().isoformat()
        self.graph = graph

    def create(self):
        user_node = Node("User", name=self.name, email=self.email, created_at=self.created_at)
        self.graph.create(user_node)
        return user_node

    def add_friend(self, friend_name):
        user_node = self.graph.nodes.match("User", name=self.name).first()
        friend_node = self.graph.nodes.match("User", name=friend_name).first()
        if user_node and friend_node:
            friends_rel = Relationship(user_node, "FRIENDS_WITH", friend_node)
            self.graph.create(friends_rel)
            return f"{self.name} and {friend_name} are now friends."
        else:
            return "User or friend not found."

    def like_post(self, post_title):
        user_node = self.graph.nodes.match("User", name=self.name).first()
        post_node = self.graph.nodes.match("Post", title=post_title).first()
        if user_node and post_node:
            likes_rel = Relationship(user_node, "LIKES", post_node)
            self.graph.create(likes_rel)
            return f"{self.name} liked the post '{post_title}'."
        else:
            return "User or post not found."

    def like_comment(self, comment_content):
        user_node = self.graph.nodes.match("User", name=self.name).first()
        comment_node = self.graph.nodes.match("Comment", content=comment_content).first()
        if user_node and comment_node:
            likes_rel = Relationship(user_node, "LIKES", comment_node)
            self.graph.create(likes_rel)
            return f"{self.name} liked the comment: '{comment_content}'."
        else:
            return "User or comment not found."


class Post:
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = datetime.utcnow().isoformat()
        self.graph = graph

    def create(self):
        user_node = self.graph.nodes.match("User", name=self.user_id).first()
        post_node = Node("Post", title=self.title, content=self.content, created_at=self.created_at)
        self.graph.create(post_node)
        created_rel = Relationship(user_node, "CREATED", post_node)
        self.graph.create(created_rel)
        return post_node


class Comment:
    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
        self.created_at = datetime.utcnow().isoformat()
        self.graph = graph

    def create(self):
        user_node = self.graph.nodes.match("User", name=self.user_id).first()
        post_node = self.graph.nodes.match("Post", title=self.post_id).first()
        comment_node = Node("Comment", content=self.content, created_at=self.created_at)
        self.graph.create(comment_node)
        created_rel = Relationship(user_node, "CREATED", comment_node)
        self.graph.create(created_rel)
        has_comment_rel = Relationship(post_node, "HAS_COMMENT", comment_node)
        self.graph.create(has_comment_rel)
        return comment_node
