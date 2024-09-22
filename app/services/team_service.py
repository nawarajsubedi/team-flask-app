from app.models import Team
from app.extensions import db
from app.services.player_service import PlayerService
from app.services.team_generation_service import generate_balanced_teams


class TeamService:

    def get_teams(self, user_id, search_name=None):
        query = Team.query.filter_by(created_by=user_id)
        if search_name:
            query = query.filter(Team.name.ilike(f"%{search_name}%"))
        return query.all()

    def get_team_by_id(self, team_id, user_id):
        return Team.query.filter_by(id=team_id, created_by=user_id).first()

    def create_team(self, name, user_id):
        new_team = Team(name=name, created_by=user_id)
        db.session.add(new_team)
        db.session.commit()
        return new_team

    def update_team(self, team_id, user_id, name):
        team = self.get_team_by_id(team_id, user_id)
        if not team:
            return None

        team.name = name

        db.session.commit()
        return team

    def delete_team(self, team_id, user_id):
        team = self.get_team_by_id(team_id, user_id)
        if not team:
            return False

        db.session.delete(team)
        db.session.commit()
        return True

    def get_teams_by_ids(self, team_ids):
        query = Team.query.filter(Team.id.in_(team_ids))
        return query.all()

    def generate_teams(self, team_ids):
        player_service = PlayerService()
        players = player_service.get_players()

        for player in players:
            print(
                f"ID: {player.id}, Name: {player.name}, Skill Level: {player.skill_level}, Created By: {player.created_by}"
            )

        print("all players", players)
        teams = self.get_teams_by_ids(team_ids)
        balanced_team = generate_balanced_teams(players, len(team_ids), teams)
        return balanced_team
