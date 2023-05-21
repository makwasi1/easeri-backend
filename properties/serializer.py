from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'subscription_status', 'created', 'updated',  'image','user']
