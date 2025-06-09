from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from jsonschema import validate, ValidationError as JsonSchemaValidationError
from django.core.exceptions import ValidationError

# jsonschema e библиотека, която си инсталирах, за да мога да задам custom json format-и

def validate_moves_schema(value):
    schema = {
        "type": "array",
        "maxItems": 9,
        "items": {
            "type": "object",
            "properties": {
                "position": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9
                },
                "player": {
                    "type": "string",
                    "enum": ["player_x", "player_o"]
                },
                "turn": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9
                },
                "symbol": {
                    "type": "string",
                    "enum": ["X", "O"]
                }
            },
            "required": ["position", "player", "turn", "symbol"]
        }
    }

    try:
        validate(instance=value, schema=schema)
    except JsonSchemaValidationError as e:
        raise ValidationError(f"Invalid move data: {e.message}")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

class Game(models.Model):
    player_x = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='games_as_x')
    player_o = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='games_as_o')
    moves = models.JSONField(
        default=list,
        validators=[validate_moves_schema]
    )
    winner = models.CharField(
        max_length=1, 
        null=True, 
        blank=True,
        choices=[('X', 'X'), ('O', 'O')]
    )


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='recieved', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_user', 'to_user')