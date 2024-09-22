from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    teams = db.relationship("Team", backref="creator_admin", foreign_keys='Team.created_by', lazy=True)
    players = db.relationship("Player", backref="creator_admin", foreign_keys='Player.created_by', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    skill_level = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)

    creator = relationship("Admin", back_populates="players")

    def __repr__(self):
        return f"<Player {self.name}>"


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    modified_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=True)
    
    players = db.relationship("Player", secondary="team_player", backref="teams")

    def __repr__(self):
        return f"<Team {self.name}>"


class TeamPlayer(db.Model):
    __tablename__ = "team_player"

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), primary_key=True)

    def __repr__(self):
        return f"<TeamPlayer Team ID {self.team_id}, Player ID {self.player_id}>"
