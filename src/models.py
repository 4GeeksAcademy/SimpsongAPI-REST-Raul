from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_table = Table(                                                 # TABLA AUXILIAR para relación muchos-a-muchos (usuarios <-> personajes)
    "favorites",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)

favorite_episode_table = Table(                                         # TABLA AUXILIAR para relación muchos-a-muchos (usuarios <-> episodios)
    "favorite_episodes",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("episode_id", ForeignKey("episode.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="author")             # relaciones uno-a-muchos
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="author")

    favorites: Mapped[list["Character"]] = relationship(  # relationship MANY TO MANY
        "Character",
        secondary=favorite_table,
        back_populates="favorited_by"
    )

    favorites_episodes: Mapped[list["Episode"]] = relationship(
        "Episode",
        secondary=favorite_episode_table,
        back_populates="favorited_by",
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "favorites": [c.serialize() for c in self.favorites],
            "favorites_episodes": [e.serialize() for e in self.favorites_episodes],
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=True)
    quote: Mapped[str] = mapped_column(String(120), nullable=True)
    image: Mapped[str] = mapped_column(String(120), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(  # relationship del otro lado (cambiamos el nombre para referenciar inversamente)
        "User",
        secondary=favorite_table,
        back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image,
        }


class Episode(db.Model):
    __tablename__ = "episode"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    season: Mapped[int] = mapped_column(Integer, nullable=False)
    episode_number: Mapped[int] = mapped_column(Integer, nullable=False)
    air_date: Mapped[str] = mapped_column(String(50), nullable=True)
    synopsis: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String(255), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_episode_table,
        back_populates="favorites_episodes",
    )

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "season": self.season,
            "episode_number": self.episode_number,
            "air_date": self.air_date,
            "synopsis": self.synopsis,
            "image": self.image,
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post",)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "author_id": self.author_id,
            "comments": [c.serialize() for c in self.comments],
        }
