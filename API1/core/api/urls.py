from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import HomeViewset, BuscarModelosViewset

router = DefaultRouter()
router.register("", HomeViewset, basename="home")

enviar_marcas = HomeViewset.as_view({
    'post': 'create'
})
buscar_modelo = BuscarModelosViewset.as_view({
    'get': 'list'
})

urlpatterns = [
    path('', include(router.urls)),
    path('enviar-marcas', enviar_marcas, name='enviar_marcas'),
    path('buscar-modelo', buscar_modelo, name='buscar_modelo'),
]
