# Teste técnico Python + Django

Sistema usando Python 3.6+ e Django 4+.

Obs: Optei por usar o python 3.8, pois o 3.6 não é compativel com Django 4. (veja)[https://docs.djangoproject.com/en/5.2/releases/4.0/#python-compatibility]

## Executar:

```shell

python -m venv .venv && source .venv/bin/activate

```

## Sistema:

### Controle de usuarios:
- [] O sitema tem dois usuários. 
  - [] (Empresa & Candidato) 
  - [] (Admin)

### Core:
*Cadastro de usuario*
- [] Obrigatório o cadastro com email (username = email) e senha.

*Cadastro de vagas*
- [] Empresa deve criar uma (ou várias) vagas.

*Candidatar para a vaga*
- [] Candidato deve se candidatar a uma (ou mais) vagas.

*Vaga*
- [] A vaga que a empresa vai criar deve ter:
  - [] Nome da vaga
  - [] Faixa salarial:
    - [] Até 1.000
    - [] De 1.000 a 2.000
    - [] De 2.000 a 3.000
    - [] Acima de 3.000
  - [] Requisitos
  - [] Escolaridade mínima:
    - [] Ensino fundamental
    - [] Ensino médio
    - [] Tecnólogo
    - [] Ensino Superior
    - [] Pós / MBA / Mestrado
    - [] Doutorado

*Candidatar*
- [] O candidato deve informar:
  - [] Pretensão salarial
  - [] Experiência
  - [] Última Escolaridade


### Objetivos:

- [] Tela de vagas com número de candidatos.

- [] Ser possível acessar quais candidatos (todos os dados) estão na vaga.
  
- [] A empresa tem o poder de editar ou deletar as vagas.

- [] Tela para relatório: implantar o Charts js(ou semelhante) gerando os seguintes gráficos:
  - [] Vagas criadas por mês
  - [] Candidatos recebidos por mês

- [] Sistema de pontos (Bônus) |- conseguir pontuar quais candidatos estão dentro do perfil da vaga (faixa salarial + escolaridade):
- [] (Default) Candidatos = 0 pontos
- [] Se dentro da faixa salarial, adiciona 1 ponto
- [] Se dentro ou acima da escolaridade, adiciona 1 ponto



## Utils scripts

Limpar migrations:
```shell
rm -r accounts/migrations/
rm -r jobs/migrations/

rm db.sqlite3

```

Criar migrations:
```shell
python3 manage.py makemigrations accounts jobs

python3 manage.py migrate
```

Criar super usuario para acessar o admin:
```shell
python3 manage.py createsuperuser

```

Levantar servidor:
```shell
python3 manage.py runserver

```

Executar os testes:
```shell
python3 manage.py test

```
