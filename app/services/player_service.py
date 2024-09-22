from app.models import Player
from app.extensions import db


class PlayerService:

    def get_players(self):
        query = Player.query.all()
        return query
    
    def get_player_by_id(self, player_id, user_id):
        return Player.query.filter_by(id=player_id, created_by=user_id).first()

    def create_player(self, name, skill_level, user_id):
        new_player = Player(
            name=name,
            skill_level=skill_level,
            created_by=user_id
        )
        db.session.add(new_player)
        db.session.commit()
        return new_player

    def update_player(self, player_id, user_id, name=None, skill_level=None):
        player = self.get_player_by_id(player_id, user_id)
        if not player:
            return None

        if name:
            player.name = name
        if skill_level:
            player.skill_level = skill_level

        db.session.commit()
        return player

    def delete_player(self, player_id, user_id):
        player = self.get_player_by_id(player_id, user_id)
        if not player:
            return False

        db.session.delete(player)
        db.session.commit()
        return True