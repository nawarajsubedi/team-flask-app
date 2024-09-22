from flask import Blueprint, request, jsonify, g
from flask import Blueprint, g, request

from app.utils import (
    create_response,
)
from app.schemas import UserSchema, PlayerSchema, TeamSchema
from app.decorators.auth import generate_jwt_token, token_required
from app.services.user_service import authenticate_user, register_user
from app.services.player_service import PlayerService
from app.services.team_service import TeamService

main_bp = Blueprint("main", __name__)

player_service = PlayerService()
team_service = TeamService()
player_schema = PlayerSchema()
team_schema = TeamSchema()


# Get all players
@main_bp.route("/players", methods=["GET"])
@token_required
def get_all_players():
    user = g.user
    try:
        players = player_service.get_players()
        players_data = player_schema.dump(players, many=True)
        return create_response("Players retrieved successfully", 200, data=players_data)
    except Exception as e:
        return create_response(
            "An error occurred while retrieving players.", 500, error=str(e)
        )


# Get a specific player by ID
@main_bp.route("/players/<int:player_id>", methods=["GET"])
@token_required
def get_player(player_id):
    user = g.user
    try:
        player = player_service.get_player_by_id(player_id=player_id, user_id=user.id)
        if player:
            player_data = player_schema.dump(player)
            return create_response(
                "Player retrieved successfully", 200, data=player_data
            )
        return create_response("Player not found", 404)
    except Exception as e:
        return create_response(
            "An error occurred while retrieving the player.", 500, error=str(e)
        )


# Create a new player
@main_bp.route("/players", methods=["POST"])
@token_required
def create_player():
    user = g.user
    try:
        json_data = request.get_json()
        new_player = player_service.create_player(
            name=json_data.get("name", ""),
            skill_level=json_data.get("skill_level", 0),
            user_id=user.id,
        )
        player_data = player_schema.dump(new_player)
        return create_response("Player created successfully", 201, data=player_data)
    except Exception as e:
        return create_response(
            "An error occurred while creating the player.", 500, error=str(e)
        )


# Update an existing player
@main_bp.route("/players/<int:player_id>", methods=["PUT"])
@token_required
def update_player(player_id):
    user = g.user
    json_data = request.get_json()
    try:
        updated_player = player_service.update_player(
            player_id=player_id,
            user_id=user.id,
            name=json_data.get("name"),
            skill_level=json_data.get("skill_level"),
        )
        updated_player_data = player_schema.dump(updated_player)
        return create_response(
            "Player updated successfully", 200, data=updated_player_data
        )
    except Exception as e:
        return create_response(
            "An error occurred while updating the player.", 500, error=str(e)
        )


# Delete a player
@main_bp.route("/players/<int:player_id>", methods=["DELETE"])
@token_required
def delete_player(player_id):
    user = g.user
    try:
        success = player_service.delete_player(player_id=player_id, user_id=user.id)
        if success:
            return create_response("Player deleted successfully", 200)
        else:
            return create_response("Player not found or not authorized to delete", 404)
    except Exception as e:
        return create_response(
            "An error occurred while deleting the player.", 500, error=str(e)
        )


# Get all teams
@main_bp.route("/teams", methods=["GET"])
@token_required
def get_all_teams():
    user = g.user
    try:
        search_name = request.args.get("search_name")
        teams = team_service.get_teams(user_id=user.id, search_name=search_name)
        teams_data = team_schema.dump(teams, many=True)
        return create_response("Teams retrieved successfully", 200, data=teams_data)
    except Exception as e:
        return create_response(
            "An error occurred while retrieving teams.", 500, error=str(e)
        )


# Get a specific team by ID
@main_bp.route("/teams/<int:team_id>", methods=["GET"])
@token_required
def get_team(team_id):
    user = g.user
    try:
        team = team_service.get_team_by_id(team_id=team_id, user_id=user.id)
        if team:
            team_data = team_schema.dump(team)
            return create_response("Team retrieved successfully", 200, data=team_data)
        return create_response("Team not found", 404)
    except Exception as e:
        return create_response(
            "An error occurred while retrieving the team.", 500, error=str(e)
        )


# Create a new team
@main_bp.route("/teams", methods=["POST"])
@token_required
def create_team():
    user = g.user
    try:
        json_data = request.get_json()
        new_team = team_service.create_team(
            name=json_data.get("name", ""),
            user_id=user.id,
        )
        team_data = team_schema.dump(new_team)
        return create_response("Team created successfully", 201, data=team_data)
    except Exception as e:
        print(f"error:{e}")
        return create_response(
            "An error occurred while creating the team.", 500, error=str(e)
        )


# Update an existing team
@main_bp.route("/teams/<int:team_id>", methods=["PUT"])
@token_required
def update_team(team_id):
    user = g.user
    json_data = request.get_json()
    try:
        updated_team = team_service.update_team(
            team_id=team_id,
            user_id=user.id,
            name=json_data.get("name"),
        )
        updated_team_data = team_schema.dump(updated_team)
        return create_response("Team updated successfully", 200, data=updated_team_data)
    except Exception as e:
        print(f"error:{e}")
        return create_response(
            "An error occurred while updating the team.", 500, error=str(e)
        )


# Delete a team
@main_bp.route("/teams/<int:team_id>", methods=["DELETE"])
@token_required
def delete_team(team_id):
    user = g.user
    try:
        success = team_service.delete_team(team_id=team_id, user_id=user.id)
        if success:
            return create_response("Team deleted successfully", 200)
        else:
            return create_response("Team not found or not authorized to delete", 404)
    except Exception as e:
        return create_response(
            "An error occurred while deleting the team.", 500, error=str(e)
        )


@main_bp.route("/teams/generation", methods=["POST"])
def team_generation():
    try:
        json_data = request.get_json()
        team_ids = json_data.get("team_ids")
        if team_ids:
            balanced_teams = team_service.generate_teams(team_ids)
            print("balanced_teams", balanced_teams)
            return create_response(
                "Team generated successfully", data=balanced_teams, status_code=200
            )
        else:
            return create_response("Team not found or not authorized to delete", 404)
    except Exception as e:
        print(f"error:{e}")
        return create_response(
            "An error occurred while deleting the team.", 500, error=str(e)
        )


@main_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return create_response("Missing data", 400)

    response, status_code = register_user(username, email, password)
    return create_response(response["message"], status_code)


@main_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return create_response("Missing data", 400)

    user, error = authenticate_user(username, password)
    if error:
        return create_response(error["message"], 401)

    token = generate_jwt_token(user.id)
    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return create_response(
        "Login successful", 200, data={"user": user_data, "token": token}
    )
