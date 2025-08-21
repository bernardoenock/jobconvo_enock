# Pseudocode

## Sistema:

### Controle de usuarios:
- [x] O sitema tem dois usuários. 
  - [x] (Empresa & Candidato) 
  - [x] (Admin)

### Core:
*Cadastro de usuario*
- [x] Obrigatório o cadastro com email (username = email) e senha.

*Cadastro de vagas*
- [x] Empresa deve criar uma (ou várias) vagas.

*Candidatar para a vaga*
- [x] Candidato deve se candidatar a uma (ou mais) vagas.

*Vaga*
- [x] A vaga que a empresa vai criar deve ter:
  - [x] Nome da vaga
  - [x] Faixa salarial:
    - [x] Até 1.000
    - [x] De 1.000 a 2.000
    - [x] De 2.000 a 3.000
    - [x] Acima de 3.000
  - [x] Requisitos
  - [x] Escolaridade mínima:
    - [x] Ensino fundamental
    - [x] Ensino médio
    - [x] Tecnólogo
    - [x] Ensino Superior
    - [x] Pós / MBA / Mestrado
    - [x] Doutorado

*Candidatar*
- [x] O candidato deve informar:
  - [x] Pretensão salarial
  - [x] Experiência
  - [x] Última Escolaridade


### Objetivos:

- [x] Tela de vagas com número de candidatos.

- [x] Ser possível acessar quais candidatos (todos os dados) estão na vaga.
  
- [x] A empresa tem o poder de editar ou deletar as vagas.

- [x] Tela para relatório: implantar o Charts js(ou semelhante) gerando os seguintes gráficos:
  - [x] Vagas criadas por mês
  - [x] Candidatos recebidos por mês

- [x] Sistema de pontos (Bônus) |- conseguir pontuar quais candidatos estão dentro do perfil da vaga (faixa salarial + escolaridade):
- [x] (Default) Candidatos = 0 pontos
- [x] Se dentro da faixa salarial, adiciona 1 ponto
- [x] Se dentro ou acima da escolaridade, adiciona 1 ponto
