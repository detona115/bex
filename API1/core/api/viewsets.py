from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from ..models import Marcas
from .serializers import MarcasSerializer
from ..tasks import enviar_marcas

import requests

Base_url = 'https://parallelum.com.br/fipe/api/v1/'
Busca_modelo_url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/'
final = Base_url + 'carros/marcas'


class HomeViewset(ModelViewSet):
    serializer_class = MarcasSerializer

    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = Marcas.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        marca = request.query_params.get('marca', None)

        if marca:
            queryset = queryset.filter(nome__contains=marca)

        serializer = MarcasSerializer(queryset, many=True)

        if queryset.count() == 0 and not marca:
            response = requests.get(Base_url + 'carros/marcas')
            data = response.json()

            bulk_data = [
                Marcas(codigo=entry['codigo'],
                       nome=entry['nome'])
                for entry in data
            ]
            Marcas.objects.bulk_create(
                bulk_data
            )

            return Response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        queryset = self.get_queryset()
        marca = get_object_or_404(queryset, codigo=pk)
        serializer = MarcasSerializer(marca)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        if self.get_queryset().count() > 0:
            for result in self.get_queryset():
                data = model_to_dict(result, ['codigo', 'nome'])
                enviar_marcas.delay('http://webapi2:8001/api/receber-marcas', data)
            return Response(
                {'message': 'marcas enviadas com sucesso!'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Não tem dados a serem enviados!'},
            status=status.HTTP_404_NOT_FOUND
        )


class BuscarModelosViewset(ModelViewSet):

    def list(self, request, *args, **kwargs):
        marca = request.query_params.get('marca', None)

        if marca:
            response = requests.get(
                f'http://webapi2:8001/api/buscar-modelo?codigo_marca={marca}'
            )
            data = response.json()
            return Response(data)

        return Response(
            {'message': 'codigo da marca não fornecido!'},
            status=status.HTTP_400_BAD_REQUEST
        )
