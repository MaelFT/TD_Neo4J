from py2neo import Graph, Node, Relationship
from datetime import datetime

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.utcnow().isoformat()

    def create(self):
        user_node = Node("User", name=self.name, email=self.email, created_at=self.created_at)
        graph.create(user_node)
        return user_node

    def like_post(self, post_title):
        user_node = graph.nodes.match("User", name=self.name).first()
        post_node = graph.nodes.match("Post", title=post_title).first()
        if user_node and post_node:
            rel = Relationship(user_node, "LIKES", post_node)
            graph.create(rel)
            return f"{self.name} liked {post_title}"
        return "User or post not found"

    def like_comment(self, comment_content):
        user_node = graph.nodes.match("User", name=self.name).first()
        comment_node = graph.nodes.match("Comment", content=comment_content).first()
        if user_node and comment_node:
            rel = Relationship(user_node, "LIKES", comment_node)
            graph.create(rel)
            return f"{self.name} liked comment: {comment_content}"
        return "User or comment not found"


class Post:
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = datetime.utcnow().isoformat()

    def create(self):
        user_node = graph.nodes.match("User", name=self.user_id).first()
        post_node = Node("Post", title=self.title, content=self.content, created_at=self.created_at)
        graph.create(post_node)
        if user_node:
            created_rel = Relationship(user_node, "CREATED", post_node)
            graph.create(created_rel)
        return post_node


class Comment:
    def __init__(self, content, user_id, post_title):
        self.content = content
        self.user_id = user_id
        self.post_title = post_title
        self.created_at = datetime.utcnow().isoformat()

    def create(self):
        user_node = graph.nodes.match("User", name=self.user_id).first()
        post_node = graph.nodes.match("Post", title=self.post_title).first()
        comment_node = Node("Comment", content=self.content, created_at=self.created_at)
        graph.create(comment_node)
        if user_node:
            graph.create(Relationship(user_node, "CREATED", comment_node))
        if post_node:
            graph.create(Relationship(post_node, "HAS_COMMENT", comment_node))
        return comment_node
