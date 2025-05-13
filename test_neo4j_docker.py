from py2neo import Graph, Node, Relationship
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter(indent=2)

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def clear_db():
    print("🧹 Suppression de tous les nœuds...")
    graph.run("MATCH (n) DETACH DELETE n")
    
def create_user(name, email):
    user = Node("User", name=name, email=email, created_at=datetime.utcnow().isoformat())
    graph.create(user)
    print(f"👤 Utilisateur créé : {name}")
    return user

def create_post(title, content, user_node):
    post = Node("Post", title=title, content=content, created_at=datetime.utcnow().isoformat())
    graph.create(post)
    rel = Relationship(user_node, "CREATED", post)
    graph.create(rel)
    print(f"📝 Post créé par {user_node['name']} : {title}")
    return post

def create_comment(content, user_node, post_node):
    comment = Node("Comment", content=content, created_at=datetime.utcnow().isoformat())
    graph.create(comment)
    graph.create(Relationship(user_node, "CREATED", comment))
    graph.create(Relationship(post_node, "HAS_COMMENT", comment))
    print(f"💬 Commentaire ajouté par {user_node['name']} sur le post '{post_node['title']}'")
    return comment

def like_post(user_node, post_node):
    rel = Relationship(user_node, "LIKES", post_node)
    graph.create(rel)
    print(f"👍 {user_node['name']} aime le post '{post_node['title']}'")

def add_friend(user1, user2):
    rel = Relationship(user1, "FRIENDS_WITH", user2)
    graph.create(rel)
    print(f"🤝 Amitié créée entre {user1['name']} et {user2['name']}")

def display_users():
    print("\n📋 Liste des utilisateurs :")
    users = graph.run("MATCH (u:User) RETURN u.name AS name, u.email AS email").data()
    pp.pprint(users)

def display_posts():
    print("\n📰 Liste des posts :")
    posts = graph.run("""
        MATCH (u:User)-[:CREATED]->(p:Post)
        RETURN u.name AS author, p.title AS title, p.content AS content
    """).data()
    pp.pprint(posts)

def display_comments():
    print("\n💬 Commentaires sur les posts :")
    comments = graph.run("""
        MATCH (u:User)-[:CREATED]->(c:Comment)<-[:HAS_COMMENT]-(p:Post)
        RETURN u.name AS author, p.title AS post_title, c.content AS comment
    """).data()
    pp.pprint(comments)

if __name__ == "__main__":
    clear_db()

    alice = create_user("Alice", "alice@example.com")
    bob = create_user("Bob", "bob@example.com")
    charlie = create_user("Charlie", "charlie@example.com")

    add_friend(alice, bob)
    add_friend(bob, charlie)

    post1 = create_post("Premier post", "Bienvenue sur mon blog !", alice)
    post2 = create_post("Hello world", "Ceci est mon premier post Neo4j.", bob)

    like_post(bob, post1)
    like_post(charlie, post1)
    like_post(alice, post2)

    create_comment("Bravo Alice !", bob, post1)
    create_comment("Hâte de lire la suite.", charlie, post1)

    display_users()
    display_posts()
    display_comments()
