from flask import Blueprint, jsonify, request
from models import User, Character, Episode, db

api = Blueprint("api", __name__)

# USERS

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@api.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.id,
        "favorite_people": [c.serialize() for c in user.favorites],
        "favorite_episodes": [e.serialize() for e in user.favorites_episodes]
    }), 200



# PEOPLE Character


@api.route("/people", methods=["GET"])
def list_people():
    people = Character.query.all()
    return jsonify([p.serialize() for p in people]), 200


@api.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# EPISODES

@api.route("/episodes", methods=["GET"])
def list_episodes():
    episodes = Episode.query.all()
    return jsonify([e.serialize() for e in episodes]), 200


@api.route("/episodes/<int:episode_id>", methods=["GET"])
def get_episode(episode_id):
    episode = Episode.query.get(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.serialize()), 200


@api.route("/favorite/episode/<int:episode_id>", methods=["POST"])
def add_favorite_episode(episode_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    episode = Episode.query.get(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    if episode in user.favorites_episodes:
        return jsonify({"message": "Already in favorites"}), 200

    user.favorites_episodes.append(episode)
    db.session.commit()

    return jsonify({"message": "Episode added to favorites"}), 201


@api.route("/favorite/episode/<int:episode_id>", methods=["DELETE"])
def delete_favorite_episode(episode_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    episode = Episode.query.get(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    if episode not in user.favorites_episodes:
        return jsonify({"error": "Favorite not found"}), 404

    user.favorites_episodes.remove(episode)
    db.session.commit()

    return jsonify({"message": "Episode removed from favorites"}), 200


@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404

    if person in user.favorites:
        return jsonify({"message": "Already in favorites"}), 200

    user.favorites.append(person)
    db.session.commit()

    return jsonify({"message": "Character added to favorites"}), 201


@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404

    if person not in user.favorites:
        return jsonify({"error": "Favorite not found"}), 404

    user.favorites.remove(person)
    db.session.commit()

    return jsonify({"message": "Character removed from favorites"}), 200