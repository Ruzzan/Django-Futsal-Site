from rest_framework import serializers
from match.models import Match, MatchObject

class MatchSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    futsal_name = serializers.CharField(source='futsal.name', read_only=True)
    class Meta:
        model = Match
        fields = [
            'id',
            'futsal',
            'futsal_name',
            'team_name',
            'team',
            'date',
            'start_time',
            'end_time',
            'player_count',
            'game_type',
            'timestamp',
        ]


class MatchObjectSerializer(serializers.ModelSerializer):
    opponent_name = serializers.CharField(source='opponent.name',read_only=True)
    class Meta:
        model = MatchObject
        fields = [
            'match',
            'opponent',
            'opponent_name',
        ]