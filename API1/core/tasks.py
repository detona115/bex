import requests
from celery import shared_task


@shared_task(bind=True)
def enviar_marcas(self, url, data):
    response = requests.post(url, data=data)
    return response.json()
