[![GitHub license](https://img.shields.io/badge/implemented%20by-Andy-blue)](https://www.linkedin.com/in/andy-kiaka-76a983110/)
# Bex

### Pré-requisitos 📋

Ter a versão mais recente do docker e docker compose instalado
no computador a ser usado

### Instalação e Execução 🔧

#### Após baixar , descompactar e acessar a pasta com os arquivos

N.B: Esta versão foi testada somente com macos, e deve funcionar perfeitamente em qualquer ambiente linux

- Em um terminal, execute o seguinte comando para construir as imagem e os containers   
- Antes da execução é necessário ter as portas 5672, 15672, 8000, 8001, 27017,
  desocupadas no computador para que todos os serviços possam funcionar e se comunicar
  normalmente.

```
docker-compose up --build
```

### Arquitetura e Serviços
O sistema é composto de 5 serviços cujo,
2 api web com django (webapi1 que armazena os dados em sql e webapi2 que armazena os dados em nosql),
Celery para executar tarefas de forma assincrona.
Rabbitmq para tratamento de filas e
Mongodb usado como banco dados para a webapi2.

### Endpoints e utilidade

#### API1
``` 
GET http://localhost:8000/api
```
- Mostra todas as marcas de veiculos armazenados no banco de dados.
- Caso seja a primeira vez, que está executando o sistema, primeiro 
  os dados são extraidos de https://parallelum.com.br/fipe/api/v1/carros/marcas
  e depois salvos no banco de dados.

```
POST localhost:8000/api/enviar-marcas
```
- Envia para a API2 todos os dados referentes à marcas em uma fila,
  através do celery e rabbitmq.

```
GET http://localhost:8000/api/<int>

ou 

GET http://localhost:8000/api?marca=<string>
```
- Busca as marcas armazenadas no banco de dados.
- A primeira opção faz a busca usando um número no final da url que se refere ao código da marca.
- A segunda opção faz a busca pelo nome usando uma query string.
- NB: substituir o < int > por um número e "< string >" por letras tipo Toyota.

```
GET http://localhost:8000/api/buscar-modelo?marca=<int>
```
- Retorna todos os modelos de uma marca salvo no banco de dados.
- A busca é feita usando uma query com o parametro marca que pega
  como valor o código da marca de veículo solicitado.
- NB: substituir o < int > por um número.
  
#### API2
```
PATCH http://localhost:8001/api/<int>/?codigo_modelo=<int>
body : {"nome": "AMAROK Comfor. 3.0 V6 TDI 4x4 Dies. Aut.sssss"}
```
- Atualiza os dados referentes à modelo solicitada na url
- Retorna o objeto alterado
- O primeiro int se refere ao código da marca e o segundo ao código do modelo
  
- NB: é obrigatório ter a url terminar com "/" e na sequência vir o "?" da query
- NB: tem que usar um objeto com a chave - valor do item que deseja alterar
      como ilustrado no exemplo acima no body da requisiçào.


## Autor ✒️

* **Andy Kiaka** - *Job Completo* - [detona115](https://github.com/detona115)

