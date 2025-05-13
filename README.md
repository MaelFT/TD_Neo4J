# 📊 Réseau Social avec Neo4j, Flask et Py2neo

Ce projet est une application de type mini-réseau social utilisant **Neo4j** comme base de données orientée graphes, **Flask** comme framework backend web, et **Py2neo** pour l'interaction avec Neo4j. Il permet de gérer des utilisateurs, des posts, des commentaires, des likes et des relations d’amitié.

## 📁 Structure du projet

```
.
├── app.py                # API Flask pour interagir avec la base de données
├── models.py             # Modèles pour les entités : User, Post, Comment
├── test_neo4j_docker.py  # Script de test pour peupler la base et visualiser les données
└── requirements.txt      # (à créer) Dépendances Python
```

## 🧰 Technologies utilisées

- Python 3
- Flask
- Neo4j
- Py2neo
- Docker (optionnel)

## 🚀 Installation et exécution

### 1. Lancer Neo4j en Docker

```bash
docker run \
  --name neo4j \
  -p7474:7474 -p7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -d neo4j
```

Interface : http://localhost:7474  
Identifiants : `neo4j / password`

### 2. Installer les dépendances Python

Créer un fichier `requirements.txt` :

```
flask
py2neo
```

Puis :

```bash
pip install -r requirements.txt
```

### 3. Lancer l’API Flask

```bash
python app.py
```

### 4. Exécuter le script de test

```bash
python test_neo4j_docker.py
```

## 🧪 Fonctionnalités

### Utilisateurs

- GET `/users` : liste des utilisateurs
- POST `/users` : créer un utilisateur
- GET `/users/<name>` : afficher un utilisateur
- PUT `/users/<name>` : mettre à jour l’email
- DELETE `/users/<name>` : supprimer un utilisateur
- POST `/users/<name>/friends` : ajouter un ami
- GET `/users/<name>/friends` : lister les amis
- GET `/users/<name>/friends/<friend_name>` : vérifier l'amitié
- DELETE `/users/<name>/friends/<friend_name>` : supprimer une amitié
- GET `/users/<name>/mutual-friends/<other_name>` : amis en commun

### Publications

- GET `/posts` : liste des posts
- POST `/users/<name>/posts` : créer un post
- GET `/users/<name>/posts` : posts d’un utilisateur
- POST `/posts/<title>/like` : liker un post
- DELETE `/posts/<title>/like` : retirer un like

### Commentaires

- POST `/posts/<title>/comments` : commenter un post
- GET `/posts/<title>/comments` : lister les commentaires

## 🔬 Script de test : `test_neo4j_docker.py`

Ce script fait :

- Suppression de la base
- Création d’utilisateurs, posts, commentaires
- Création des relations (amitié, like, création)
- Affichage de tous les éléments

## ✅ Exemple de données

- Utilisateurs : Alice, Bob, Charlie
- Posts : "Premier post", "Hello world"
- Commentaires : "Bravo Alice !", "Hâte de lire la suite."
- Likes et relations d’amitié

## 📌 Remarques

- Neo4j doit être lancé **avant** d’utiliser l’API ou le script.
- Le mot de passe par défaut est : `neo4j / password`

## 📬 Auteur

Projet réalisé dans le cadre d’un TP sur Neo4j.
