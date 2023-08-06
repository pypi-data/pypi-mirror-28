# Imports from other dependencies.  # NOQA
from rest_framework import serializers


# Imports from editorial-staff.
from editorial_staff.models import Hub
from editorial_staff.models import Staffer
from editorial_staff.models import Vertical


class VerticalSerializer(serializers.ModelSerializer):
    class Meta:  # NOQA
        model = Vertical
        fields = (
            'id',
            'name',
            'slug',
            'url',
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
                'view_name': 'editorial_staff:api:v2:vertical-detail',
            }
        }


class HubSerializer(serializers.ModelSerializer):
    vertical = VerticalSerializer(many=False, read_only=True)

    class Meta:  # NOQA
        model = Hub
        fields = (
            'id',
            'color',
            'name',
            'slug',
            'vertical',
            'url',
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
                'view_name': 'editorial_staff:api:v2:hub-detail',
            }
        }


class StafferSerializer(serializers.ModelSerializer):
    formatted_name = serializers.CharField(
        source='render_formatted_name',
        read_only=True
    )

    class Meta:  # NOQA
        model = Staffer
        fields = (
            'id',
            'first_name',
            'last_name',
            'full_name',
            'formatted_name',
            'email',
            'image_url',
            'active',
            'url',
        )
        lookup_field = 'email'
        extra_kwargs = {
            'url': {
                'lookup_field': 'email',
                'view_name': 'editorial_staff:api:v2:staffer-detail',
            }
        }
