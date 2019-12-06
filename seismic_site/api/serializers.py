from rest_framework import serializers
from map_app.models import (
    Building,
    CsvFile
)


class BuildingSerializer (serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = [
            'general_id',
            'risk_category',
            'registration_number',
            'examination_year',
            'certified_expert',
            'observations',
            'lat',
            'lng',
            'county',
            'address',
            'post_code',
            'locality',
            'year_built',
            'height_regime',
            'apartment_count',
            'surface',
            'cadastre_number',
            'land_registry_number',
            'administration_update',
            'admin_update',
            'status',
        ]
        read_only_fields = [
            'general_id',
        ]


class CsvSerializer (serializers.ModelSerializer):
    class Meta:
        model = CsvFile
        fields: [
            'name',
            'file',
            'status',
        ]
