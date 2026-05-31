# Gerenciador de Tickets em Python

Projeto criado durante a trilha de estudos de IA com Python.

## Objetivo

Criar um sistema em terminal para gerenciar tickets usando Python, orientação a objetos, JSON, módulos, tipagem e organização em camadas.

Este projeto serve como preparação para a próxima fase da trilha: SQL com PostgreSQL.

## Funcionalidades

* Criar tickets
* Listar tickets
* Buscar ticket por ID
* Alterar status do ticket
* Salvar tickets em arquivo JSON
* Carregar tickets ao iniciar o programa
* Validar estrutura do JSON
* Bloquear salvamento quando o arquivo de dados estiver inválido
* Usar `Enum` para controlar status válidos
* Separar responsabilidades entre `main.py`, `TicketService` e `TicketRepository`

## Status disponíveis

Os tickets podem ter os seguintes status:

* aberto
* em andamento
* fechado

## Estrutura do projeto

```text
gerenciador_tickets/
├── main.py
├── data/
│   └── tickets.json
├── models/
│   ├── ticket.py
│   ├── tickets_status.py
│   ├── resultado_operacao.py
│   └── resultado_alteracao_status.py
└── services/
    ├── ticket_repository.py
    └── ticket_service.py
```

## Como executar

No terminal, dentro da pasta do projeto, execute:

```bash
python main.py
```

## Como usar

Ao iniciar o programa, será exibido um menu:

```text
--- Gerenciador de Tickets ---

1. Criar ticket
2. Listar tickets
3. Buscar ticket por ID
4. Alterar o status do ticket
0. Sair
```

Escolha uma opção digitando o número correspondente.

## Conceitos praticados

* Classes
* `@dataclass`
* `Enum`
* Type hints
* Listas de objetos
* Leitura e escrita de JSON
* Tratamento de exceções
* Validação de dados
* Separação em camadas
* Repository
* Service
* Resultado de operação
* Proteção contra perda de dados
* Git e GitHub

## Organização das responsabilidades

### `main.py`

Responsável pela interface de terminal:

* mostrar menu;
* receber entrada do usuário;
* converter texto digitado;
* exibir mensagens;
* chamar o `TicketService`.

### `TicketService`

Responsável pelas regras de negócio:

* validar criação de tickets;
* coordenar busca e alteração de status;
* retornar mensagens de sucesso ou erro usando `ResultadoOperacao`.

### `TicketRepository`

Responsável pela persistência dos dados:

* carregar tickets do JSON;
* validar estrutura do arquivo;
* salvar tickets no JSON;
* buscar ticket por ID;
* alterar dados persistidos;
* bloquear salvamento quando o carregamento não for seguro.

### `Ticket`

Modelo que representa um ticket:

```python
Ticket(
    id=1,
    titulo="Erro no sistema",
    descricao="Descrição do problema",
    status=TicketStatus.ABERTO
)
```

## Proteção contra perda de dados

O sistema bloqueia o salvamento quando encontra problemas no arquivo `tickets.json`, como:

* JSON mal formatado;
* estrutura diferente de lista;
* campos obrigatórios ausentes;
* tipos incorretos;
* status inválido.

Isso evita que o programa sobrescreva um arquivo com problemas e apague dados antigos por acidente.

## Tecnologias usadas

* Python
* JSON
* Dataclasses
* Enum
* Git

## Próximos passos

Este projeto será usado como base conceitual para estudar:

* SQL
* PostgreSQL
* persistência em banco de dados
* CRUD
* APIs com FastAPI
