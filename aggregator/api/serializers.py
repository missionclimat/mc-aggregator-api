from api.models import Workshop, Result
from rest_framework import serializers


class WorkshopSerializer(serializers.ModelSerializer):
    results = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='data'
     )

    class Meta:

        model = Workshop
        fields = ['id', 'workshop_code', 'admin_code', 'results', 'workshop_name', 'admin_name', 'admin_email', 'participants_nb']

class ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Result
        fields = ["id", "data", "workshop_code", "user_email", "group_name"]



# Only for documentation
class WorkshopSerializerWithoutResults(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ['id', 'workshop_code', 'admin_code', 'workshop_name', 'admin_name', 'admin_email', 'participants_nb']



class WorkshopsAndResultsSerializer(serializers.Serializer):

    workshops = WorkshopSerializerWithoutResults(many=True)
    results = ResultSerializer(many=True)