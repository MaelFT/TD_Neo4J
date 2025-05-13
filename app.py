from flask import Flask, request, jsonify
from models import User, Post, Comment
from py2neo import Graph, Relationship

app = Flask(__name__)
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))


@app.route('/users', methods=['GET'])
def get_users():
    users = graph.nodes.match("User")
    return jsonify([dict(user) for user in users])


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(data['name'], data['email'])
    node = user.create()
    return jsonify(dict(node)), 201


@app.route('/users/<name>', methods=['GET'])
def get_user(name):
    user = graph.nodes.match("User", name=name).first()
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404


@app.route('/users/<name>', methods=['PUT'])
def update_user(name):
    data = request.get_json()
    user = graph.nodes.match("User", name=name).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user['email'] = data.get('email', user['email'])
    graph.push(user)
    return jsonify(dict(user))


@app.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    user = graph.nodes.match("User", name=name).first()
    if user:
        graph.delete(user)
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404


@app.route('/users/<name>/friends', methods=['POST'])
def add_friend(name):
    data = request.get_json()
    friend_name = data['friend_id']
    user = graph.nodes.match("User", name=name).first()
    friend = graph.nodes.match("User", name=friend_name).first()
    if user and friend:
        rel = Relationship(user, "FRIENDS_WITH", friend)
        graph.create(rel)
        return jsonify({"message": f"{name} and {friend_name} are now friends."}), 201
    return jsonify({"error": "User or friend not found"}), 404


@app.route('/users/<name>/friends', methods=['GET'])
def list_friends(name):
    query = """
    MATCH (:User {name: $name})-[:FRIENDS_WITH]->(f:User)
    RETURN f.name AS name, f.email AS email
    """
    result = graph.run(query, name=name).data()
    return jsonify(result)


@app.route('/users/<name>/friends/<friend_name>', methods=['GET'])
def are_friends(name, friend_name):
    query = """
    MATCH (:User {name: $name})-[:FRIENDS_WITH]->(:User {name: $friend})
    RETURN count(*) AS c
    """
    res = graph.run(query, name=name, friend=friend_name).evaluate()
    return jsonify({"are_friends": res > 0})


@app.route('/users/<name>/friends/<friend_name>', methods=['DELETE'])
def remove_friend(name, friend_name):
    query = """
    MATCH (u:User {name: $name})-[r:FRIENDS_WITH]->(f:User {name: $friend})
    DELETE r
    """
    graph.run(query, name=name, friend=friend_name)
    return jsonify({"message": "Friend removed"})


@app.route('/users/<name>/mutual-friends/<other_name>', methods=['GET'])
def mutual_friends(name, other_name):
    query = """
    MATCH (u1:User {name: $name})-[:FRIENDS_WITH]->(f:User)<-[:FRIENDS_WITH]-(u2:User {name: $other})
    RETURN f.name AS name, f.email AS email
    """
    result = graph.run(query, name=name, other=other_name).data()
    return jsonify(result)


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = graph.nodes.match("Post")
    return jsonify([dict(post) for post in posts])


@app.route('/users/<name>/posts', methods=['POST'])
def create_post(name):
    data = request.get_json()
    post = Post(data['title'], data['content'], name)
    node = post.create()
    return jsonify(dict(node)), 201


@app.route('/users/<name>/posts', methods=['GET'])
def user_posts(name):
    query = """
    MATCH (u:User {name: $name})-[:CREATED]->(p:Post)
    RETURN p.title AS title, p.content AS content, p.created_at AS created_at
    """
    result = graph.run(query, name=name).data()
    return jsonify(result)


@app.route('/posts/<title>/like', methods=['POST'])
def like_post(title):
    data = request.get_json()
    user = User(data['user_id'], "")
    return jsonify({"message": user.like_post(title)})


@app.route('/posts/<title>/like', methods=['DELETE'])
def unlike_post(title):
    data = request.get_json()
    query = """
    MATCH (u:User {name: $user})-[r:LIKES]->(p:Post {title: $title})
    DELETE r
    """
    graph.run(query, user=data['user_id'], title=title)
    return jsonify({"message": "Like removed"})


@app.route('/posts/<title>/comments', methods=['POST'])
def add_comment(title):
    data = request.get_json()
    comment = Comment(data['content'], data['user_id'], title)
    node = comment.create()
    return jsonify(dict(node)), 201


@app.route('/posts/<title>/comments', methods=['GET'])
def get_comments(title):
    query = """
    MATCH (:Post {title: $title})-[:HAS_COMMENT]->(c:Comment)
    RETURN c.content AS content, c.created_at AS created_at
    """
    result = graph.run(query, title=title).data()
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
