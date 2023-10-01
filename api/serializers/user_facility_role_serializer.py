from rest_framework.serializers import ModelSerializer

from api.models.user_facility_role import UserFacilityRole


class UserFacilityRoleSerializer(ModelSerializer):
    class Meta:
        model = UserFacilityRole
        fields = (
            'user_id',
            'facility_id',
            'role_id',
        )