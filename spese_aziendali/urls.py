from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriaSpesaViewSet, RichiestaRimborsoViewSet, StatisticheRimborsiView,)

router = DefaultRouter()
router.register(r"rimborsi", RichiestaRimborsoViewSet, basename="rimborsi")
router.register(r"categorie-spesa", CategoriaSpesaViewSet, basename="categorie")

urlpatterns = [
    path("", include(router.urls)),
    path("statistiche/rimborsi/", StatisticheRimborsiView.as_view()),
]