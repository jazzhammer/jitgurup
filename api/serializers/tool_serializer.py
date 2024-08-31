import rest_framework.serializers

from api.models.tool import Tool


class ToolSerializer(rest_framework.serializers.ModelSerializer):

    class Meta:
        model = Tool

        fields = [
            'name'
        ]
