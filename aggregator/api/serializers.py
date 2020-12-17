from api.models import Workshop, Result
from rest_framework import serializers


class WorkshopSerializer(serializers.ModelSerializer):
    results = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='data'
     )
    class Meta:

        # Override all the schema fields if cannot override only "results" 

        # swagger_schema_fields = {
        #     "type": openapi.TYPE_OBJECT,
        #     "title": "Email",
        #     "properties": {
        #         "subject": openapi.Schema(
        #             title="Email subject",
        #             type=openapi.TYPE_STRING,
        #         ),
        #         "body": openapi.Schema(
        #             title="Email body",
        #             type=openapi.TYPE_STRING,
        #         ),
        #     },
        #     "required": ["subject", "body"],
        #  }

        model = Workshop
        fields = ['id', 'workshop_code', 'admin_code', 'results', 'workshop_name', 'admin_name', 'admin_email', 'participants_nb']

class ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Result
        fields = ["id", "data", "workshop_code", "user_email", "group_name"]
