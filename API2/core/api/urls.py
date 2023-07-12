from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import HomeViewset, BuscarModeloViewset

router = DefaultRouter()
router.register("", HomeViewset, basename="home")
router.register("buscar-modelo", BuscarModeloViewset, basename='busca')
buscar_modelo = BuscarModeloViewset.as_view(
    {'get': 'list'}
)
receber_marcas = HomeViewset.as_view({
    'post': 'create'
})

urlpatterns = [
    path('', include(router.urls)),
    path('buscar-modelo', buscar_modelo, name='buscar_modelo'),
    path('receber-marcas', receber_marcas, name='receber_marcas'),
]
