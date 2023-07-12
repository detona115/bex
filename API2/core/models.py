
from django.db import models


class Marcas(models.Model):
    codigo = models.CharField(max_length=250, unique=True)
    nome = models.CharField(max_length=250)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Modelo(models.Model):
    codigo = models.CharField(max_length=250)
    nome = models.CharField(max_length=250)
    marca = models.ForeignKey(
        Marcas,
        on_delete=models.CASCADE,
        related_name='modelo',
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f'{self.codigo} - {self.nome} - {self.marca.nome}'


class Ano(models.Model):
    codigo = models.CharField(max_length=250)
    nome = models.CharField(max_length=250)
    marca = models.ForeignKey(
        Marcas,
        on_delete=models.CASCADE,
        related_name='ano',
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f'{self.codigo} - {self.nome} - {self.marca.nome}'
