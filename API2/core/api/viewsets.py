import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Marcas, Modelo, Ano
from .serializers import MarcasSerializer, ModeloSerializer

Base_url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/'


class HomeViewset(ModelViewSet):
    serializer_class = MarcasSerializer
    queryset = Marcas.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = MarcasSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        queryset = self.get_queryset()
        marca = get_object_or_404(queryset, codigo=pk)
        serializer = MarcasSerializer(marca)
        return Response(serializer.data)

    def partial_update(self, request, pk):
        codigo_modelo = request.query_params.get('codigo_modelo', None)
        if codigo_modelo:
            partial = True
            item = get_object_or_404(Marcas.objects.filter(modelo__codigo=codigo_modelo), codigo=pk)
            serializer = MarcasSerializer(item, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'invalid query param'},
            status=status.HTTP_404_NOT_FOUND
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = requests.get(f'{Base_url}{request.data["codigo"]}/modelos')
        data = response.json()
        modelos = data['modelos']
        anos = data['anos']
        marca = Marcas.objects.get(codigo=request.data["codigo"])

        bulk_modelos = [
            Modelo(codigo=entry['codigo'],
                   nome=entry['nome'],
                   marca=marca)
            for entry in modelos
        ]
        Modelo.objects.bulk_create(
            bulk_modelos
        )

        bulk_anos = [
            Ano(codigo=entry['codigo'],
                nome=entry['nome'],
                marca=marca)
            for entry in anos
        ]
        Ano.objects.bulk_create(
            bulk_anos
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BuscarModeloViewset(ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer

    def list(self, request, *args, **kwargs):
        codigo_marca = request.query_params.get('codigo_marca', None)
        if codigo_marca:
            queryset = self.get_queryset().filter(marca__codigo=codigo_marca)
            serializer = ModeloSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            {'message': 'Invalid query param'},
            status=status.HTTP_404_NOT_FOUND
        )
