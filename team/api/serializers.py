from rest_framework import serializers, permissions, authentication
from team.models import Team, TeamMember

class TeamSerializer(serializers.ModelSerializer):
    admin = serializers.ReadOnlyField(source='admin.username')
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'admin',
            'logo',
            'bio',
            'members',
            'timestamp',
        ]

class TeamMemberSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name',read_only=True)
    user      = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = TeamMember
        fields = [
            'id',
            'team',
            'team_name',
            'user',
        ]

    

    

