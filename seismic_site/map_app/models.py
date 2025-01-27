from enum import Enum

# from django.db import models
from import_export import resources

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class SectorChoice(Enum):
    s1 = "Sector 1"
    s2 = "Sector 2"
    s3 = "Sector 3"
    s4 = "Sector 4"
    s5 = "Sector 5"
    s6 = "Sector 6"


BUILDING_STATUS_CHOICES = [(0, "Alege"), (1, "Acceptat"), (-1, "Respins")]


class SeismicCategoryChoice(Enum):
    pass
    # TODO Implement this and replace in model


class BuildingManager(models.Manager):

    def find_by_point(self, lat, lng, radius):
        user_point = Point(lng, lat)
        qs = self.filter(location__distance_lte=(user_point, Distance(km=radius)))

        return qs


class Building(models.Model):

    objects = BuildingManager()

    general_id = models.AutoField(
        primary_key=True
    )

    risk_category = models.CharField(
        max_length=50,
        db_index=True
    )
    registration_number = models.IntegerField(
        null=True
    )
    examination_year = models.IntegerField(
        null=True
    )
    certified_expert = models.CharField(
        max_length=100,
        null=True
    )
    observations = models.CharField(
        max_length=1000,
        null=True
    )

    # this will need to be modified as a GIS field
    # Reffer to geo Django for details
    lat = models.FloatField(
        null=True
    )
    lng = models.FloatField(
        null=True
    )

    location = models.PointField(
        srid=4326,
        null=True,
        blank=True
    )

    county = models.CharField(
        max_length=60
    )
    address = models.CharField(
        max_length=250,
        null=True
    )
    post_code = models.CharField(
        max_length=250
    )
    locality = models.CharField(
        max_length=20
    )

    year_built = models.IntegerField(
        null=True
    )
    height_regime = models.CharField(
        max_length=50,
        null=True
    )
    apartment_count = models.IntegerField(
        null=True
    )
    surface = models.FloatField(
        null=True
    )

    cadastre_number = models.IntegerField(
        null=True
    )
    land_registry_number = models.CharField(
        max_length=50,
        null=True
    )
    administration_update = models.DateField(
        null=True,
        blank=True
    )
    admin_update = models.DateField(
        null=True,
        blank=True
    )

    status = models.SmallIntegerField(
        default=0, choices=BUILDING_STATUS_CHOICES, db_index=True
    )

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        self.location = Point(self.lng, self.lat)
        super(Building, self).save(*args, **kwargs)


class BuildingResource(resources.ModelResource):
    class Meta:
        DATE_FORMAT = {"format": "%d.%m.%Y"}

        model = Building
        exclude = ("id",)
        import_id_fields = ("general_id",)

        widgets = {
            "administration_update": DATE_FORMAT,
            "admin_update": DATE_FORMAT,
        }


class CsvFile(models.Model):

    NOT_TRIED = 0
    SUCCESS = 1
    UNSUCCESS = -1

    STATUS_CHOICES = [
        (UNSUCCESS, "Unsuccess"),
        (NOT_TRIED, "Not tried"),
        (SUCCESS, "Success"),
    ]

    name = models.CharField(max_length=255)
    file = models.FileField()
    status = models.SmallIntegerField(
        default=NOT_TRIED, editable=False, choices=STATUS_CHOICES
    )

    def __str__(self):
        return self.name
