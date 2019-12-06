from django.urls import path
from api import views

urlpatterns = [
    path('building/', views.BuildingView.as_view()),

]
# path('crumb/<str:uuid>/', view.YourView.as_view()),
