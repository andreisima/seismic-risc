from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.pagination import PaginationHandlerMixin

from api.serializers import (
    BuildingSerializer,
    CsvSerializer,
)
from map_app.models import (
    Building,
    CsvFile
)


class BasicPagination(PageNumberPagination):

    page_size_query_param = 'limit'


class BuildingFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)
        print(request.query_params)
        if filter_class:
            return filter_class(
                request.query_params,
                queryset=queryset,
                request=request
            ).qs
        else:
            return queryset


class BuildingView(APIView, PaginationHandlerMixin):

    serializer_class = BuildingSerializer
    pagination_class = BasicPagination
    filter_fields = {
        'risk_category': ['exact', ],
        'registration_number': ['exact', ],
        'certified_expert': ['icontains', ],
    }

    def get(self, request, format=None):
        queryset = Building.objects.all()

        fqs = BuildingFilterBackend()

        filtered_queryset = fqs.filter_queryset(request, queryset, self)

        if filtered_queryset is not None:
            queryset = filtered_queryset
            serializer = self.serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(
                    page,
                    many=True
                ).data
            )
        else:
            serializer = self.serializer_class(
                queryset,
                many=True
            )

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CsvView (APIView):

    serializer_class = CsvSerializer

    def get(self, request, format=None):
        csvfiles = CsvFile.objects.all()
        serializer = self.serializer_class(
            csvfiles,
            many=True
        )

        return Response(serializer.data)