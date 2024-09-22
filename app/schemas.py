from marshmallow import fields

from app.extensions import ma
from app.models import Player, Team


class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True

    created_at = ma.DateTime(format="%Y-%m-%dT%H:%M:%S")
    modified_at = ma.DateTime(format="%Y-%m-%dT%H:%M:%S")


class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance = True

    created_at = ma.DateTime(format="%Y-%m-%dT%H:%M:%S")
    modified_at = ma.DateTime(format="%Y-%m-%dT%H:%M:%S")


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
