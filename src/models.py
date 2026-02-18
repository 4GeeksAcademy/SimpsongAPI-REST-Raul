from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_table = Table(                         #TABLA AUXILIAR 
    "favorites",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),    #COMO TENEMOS UNA FOREIGNKEY de un lado necesitaremos una relationship
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites: Mapped[list["Character"]] = relationship(                        #relationship
    "Character",
    secondary=favorite_table,
    back_populates="favorited_by"
    )                       

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [character.serialize() for character in self.favorites]
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable= False)
    quote: Mapped[str] = mapped_column(String(120), nullable = True)
    image: Mapped[str] = mapped_column(String(120), nullable = True)
    favorited_by: Mapped[list["User"]] = relationship(                        #relationship del otro lado (cambiamos el nombre para referenciar inversamente)
    "User",
    secondary=favorite_table,
    back_populates="favorites"
    )      

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image
        }