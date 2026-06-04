# Gerenciador de Tickets em Python

Projeto criado durante a trilha de estudos de IA com Python.

## Objetivo

Criar um sistema em terminal para gerenciar tickets usando Python, orientação a objetos, módulos, tipagem, validação de dados, arquitetura em camadas e persistência.

O projeto começou salvando dados em JSON e depois evoluiu para usar PostgreSQL como banco de dados principal.

Este projeto faz parte da preparação para as próximas fases da trilha:

* SQL com PostgreSQL
* FastAPI
* APIs com banco de dados
* aplicações de chatbot com persistência

## Funcionalidades

* Criar tickets
* Listar tickets
* Buscar ticket por ID
* Alterar status do ticket
* Persistir tickets em PostgreSQL
* Usar `Enum` para controlar status válidos
* Usar `Service` para regras de negócio
* Usar `Repository` para acesso aos dados
* Usar `.env` para guardar configurações sensíveis
* Usar `psycopg` para conectar Python ao PostgreSQL

## Status disponíveis

Os tickets podem ter os seguintes status:

* aberto
* em andamento
* fechado

## Estrutura do projeto

```text
gerenciador_tickets/
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── tickets.json
├── models/
│   ├── ticket.py
│   ├── tickets_status.py
│   ├── resultado_operacao.py
│   └── resultado_alteracao_status.py
└── services/
    ├── ticket_repository.py
    ├── ticket_postgres_repository.py
    └── ticket_service.py
```

## Persistência de dados

O projeto possui dois repositórios:

### `TicketRepository`

Versão baseada em JSON.

Responsável por:

* carregar tickets de `data/tickets.json`;
* validar estrutura do JSON;
* salvar tickets no arquivo;
* proteger contra perda de dados quando o JSON está inválido.

### `TicketPostgresRepository`

Versão baseada em PostgreSQL.

Responsável por:

* listar tickets do banco;
* buscar ticket por ID;
* criar tickets com `INSERT`;
* alterar status com `UPDATE`;
* converter registros do banco em objetos `Ticket`.

Atualmente, o sistema principal usa o `TicketPostgresRepository`.

## Banco de dados

O projeto usa PostgreSQL com duas tabelas principais:

```sql
CREATE TABLE ticket_status (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status_id INT NOT NULL,
    CONSTRAINT fk_tickets_status
        FOREIGN KEY (status_id)
        REFERENCES ticket_status(id)
);
```

Também foram adicionadas constraints para evitar texto vazio:

```sql
ALTER TABLE tickets
ADD CONSTRAINT chk_titulo_nao_vazio
CHECK (length(trim(titulo)) > 0);

ALTER TABLE tickets
ADD CONSTRAINT chk_descricao_nao_vazia
CHECK (length(trim(descricao)) > 0);
```

## Configuração do ambiente

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Ou no Prompt de Comando:

```bash
.venv\Scripts\activate.bat
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

O arquivo `.env` não deve ser enviado para o GitHub.

O `.gitignore` deve conter:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## Como executar

Com o ambiente virtual ativado e o PostgreSQL configurado, execute:

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

### `TicketPostgresRepository`

Responsável pela persistência em PostgreSQL:

* executar queries SQL;
* transformar linhas do banco em objetos `Ticket`;
* inserir novos tickets;
* buscar tickets por ID;
* alterar status.

### `TicketRepository`

Responsável pela persistência em JSON.

Mantido no projeto como versão anterior e comparação didática com o repositório PostgreSQL.

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

### `TicketStatus`

Enum que representa os status válidos:

```python
TicketStatus.ABERTO
TicketStatus.EM_ANDAMENTO
TicketStatus.FECHADO
```

## Segurança e boas práticas

O projeto evita colocar senha diretamente no código.

As credenciais do banco ficam no arquivo `.env`, que deve permanecer apenas no ambiente local.

O acesso ao banco é feito com placeholders do `psycopg`, evitando montar SQL com f-string e reduzindo risco de SQL injection.

Exemplo:

```python
cursor.execute(
    "SELECT * FROM tickets WHERE id = %s;",
    (ticket_id,)
)
```

## Conceitos praticados

* Python
* Orientação a objetos
* `@dataclass`
* `Enum`
* Type hints
* JSON
* PostgreSQL
* SQL
* `SELECT`
* `INSERT`
* `UPDATE`
* `JOIN`
* `FOREIGN KEY`
* `CHECK`
* `NOT NULL`
* Repository
* Service
* Resultado de operação
* Variáveis de ambiente
* `.env`
* `python-dotenv`
* `psycopg`
* Git e GitHub

## Próximos passos

Este projeto será usado como base para estudar:

* melhorar abstração entre repositórios;
* aprofundar SQL e PostgreSQL;
* criar uma API com FastAPI;
* conectar endpoints HTTP ao banco;
* evoluir para sistemas com usuários, conversas e histórico;
* preparar a base para chatbots com persistência.
