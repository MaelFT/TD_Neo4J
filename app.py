from flask import Flask, request, jsonify
from models import User, Post
from py2neo import Graph

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    users = graph.nodes.match("User")
    users_list = [{"name": user["name"], "email": user["email"]} for user in users]
    return jsonify(users_list)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(data['name'], data['email'])
    user_node = user.create()
    return jsonify({"name": user_node["name"], "email": user_node["email"]}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    posts = graph.nodes.match("Post")
    posts_list = [{"title": post["title"], "content": post["content"]} for post in posts]
    return jsonify(posts_list)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(data['title'], data['content'], data['user_id'])
    post_node = post.create()
    return jsonify({"title": post_node["title"], "content": post_node["content"]}), 201

@app.route('/users/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    data = request.get_json()
    friend_id = data['friend_id']
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    user_node = graph.nodes.match("User", name=user_id).first()
    friend_node = graph.nodes.match("User", name=friend_id).first()
    relationship = Relationship(user_node, "FRIENDS_WITH", friend_node)
    graph.create(relationship)
    return jsonify({"message": f"{user_id} and {friend_id} are now friends."}), 201

if __name__ == '__main__':
    app.run(debug=True)
