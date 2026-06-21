# Gerenciador de Tickets em Python

Projeto desenvolvido durante a trilha de estudos de IA com Python. O sistema nasceu como uma aplicação de terminal baseada em arquivos JSON e evoluiu para uma API REST robusta utilizando arquitetura em camadas, persistência em banco de dados PostgreSQL e documentação automática.

## 🎯 Objetivo e Evolução

O principal objetivo deste projeto é praticar conceitos avançados de desenvolvimento backend com Python, servindo como base preparatória para a construção de aplicações complexas e chatbots com persistência de dados. 

A evolução do projeto seguiu os seguintes marcos:
1. **Fase 1:** Sistema em terminal com persistência local em arquivos JSON.
2. **Fase 2:** Migração da persistência para o banco de dados PostgreSQL.
3. **Fase 3:** Transformação do sistema em uma API REST completa com FastAPI e validação de dados via Pydantic.

---

## 🚀 Funcionalidades

* **Criar tickets** com validação de dados.
* **Listar todos os tickets** cadastrados.
* **Buscar ticket por ID** específico.
* **Alterar status do ticket** utilizando regras de negócio controladas.
* **Remover tickets** do banco de dados (Exclusão).
* **Persistência Relacional** robusta com PostgreSQL.
* **Documentação automatizada** da API via Swagger UI e ReDoc.

---

## 🛠️ Tecnologias e Conceitos Praticados

* **Linguagem:** Python 3 (com Type Hints e `@dataclass`).
* **Framework Web:** FastAPI & Uvicorn (Servidor ASGI).
* **Validação de Dados:** Pydantic (Schemas de entrada e saída).
* **Banco de Dados:** PostgreSQL & Driver Psycopg.
* **Gerenciamento de Ambiente:** Python Dotenv & Ambientes Virtuais (`venv`).
* **Boas Práticas:** Arquitetura em camadas, Isolamento de credenciais locais e Prevenção contra SQL Injection.

---

## 📂 Estrutura do Projeto

Abaixo está a organização atual do repositório, refletindo a migração completa para a estrutura de API:

```text
gerenciador_tickets/
├── api/
│   ├── app.py              # Inicialização do FastAPI e configurações
│   ├── dependencies.py     # Injeção de dependências (conexão com o banco, etc.)
│   └── routes/             # Definição dos endpoints HTTP (Routers)
├── data/
│   └── tickets.json        # Arquivo legado mantido para fins didáticos
├── models/                 # Modelos de domínio e Enums do sistema
│   ├── ticket.py
│   ├── tickets_status.py
│   ├── resultado_operacao.py
│   └── resultado_alteracao_status.py
├── repositories/           # Camada de persistência (JSON e Postgres)
│   ├── ticket_repository.py
│   └── ticket_postgres_repository.py
├── schemas/                # Schemas de validação do Pydantic para a API
├── services/               # Camada de regras de negócio (Services)
│   └── ticket_service.py
├── database.py             # Configuração e inicialização do pool com o PostgreSQL
├── .env                    # Variáveis de ambiente locais (não versionado)
├── .gitignore              # Proteção contra envio de arquivos sensíveis
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto

```

---

## 📐 Arquitetura e Responsabilidades

O projeto adota o padrão de separação rigorosa de responsabilidades em camadas:

```text
Request (HTTP) ──> Router ──> Service ──> Repository ──> PostgreSQL

```

### 🔹 1. Routers (`api/routes/`)

* **Responsabilidade:** Receber as requisições HTTP, expor os endpoints e retornar os códigos de status HTTP corretos (200, 201, 404, etc.).


* **Validação:** Utiliza os **Schemas (Pydantic)** para garantir que os dados recebidos e enviados estejam no formato correto.



### 🔹 2. Services (`services/`)

* **Responsabilidade:** Concentrar todas as regras de negócio do sistema (ex: validar se um ticket pode transitar de um status para outro).


* **Interface:** Coordena o fluxo de dados e utiliza classes como `ResultadoOperacao` para responder de forma limpa aos Routers.



### 🔹 3. Repositories (`repositories/`)

* **Responsabilidade:** Isolar completamente o acesso aos dados.


* `TicketPostgresRepository`: Responsável por executar queries SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) e converter registros brutos do banco em objetos do domínio Python.


* `TicketRepository`: Versão baseada em JSON mantida no projeto para comparação didática de persistência estruturada versus arquivos locais.





### 🔹 4. Models e Enums (`models/`)

* **`Ticket`:** Modelo que mapeia a entidade interna do sistema.


* **`TicketStatus`:** `Enum` que controla rigidamente as opções de status permitidas no sistema:


* `aberto`
* `em andamento`
* `fechado`



---

## 🗄️ Banco de Dados

O projeto utiliza o PostgreSQL. O banco possui duas tabelas principais fortemente relacionadas:

```text
ticket_status (1) <─────── (N) tickets

```

### Script de Inicialização (DDL)

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

### Constraints de Segurança de Dados

Para evitar o armazenamento de dados inconsistentes, foram adicionadas regras que impedem campos contendo apenas espaços vazios:

```sql
ALTER TABLE tickets
ADD CONSTRAINT chk_titulo_nao_vazio
CHECK (length(trim(titulo)) > 0);

ALTER TABLE tickets
ADD CONSTRAINT chk_descricao_nao_vazia
CHECK (length(trim(descricao)) > 0);

```

---

## 🔒 Segurança e Boas Práticas

* **Variáveis de Ambiente:** Credenciais de banco de dados e chaves sensíveis nunca são inseridas diretamente no código, sendo isoladas no arquivo `.env` local.


* **Prevenção contra SQL Injection:** Todas as interações com o banco via `psycopg` utilizam **placeholders parametrizados** `%s` em vez de f-strings ou concatenação direta de texto.



```python
  # Exemplo correto utilizado no projeto:
  cursor.execute("SELECT * FROM tickets WHERE id = %s;", (ticket_id,))

```

---

## 🛣️ Endpoints da API

### 🏥 Health Check

* `GET /health` - Verifica a saúde e a conectividade da aplicação.



### 🎫 Gerenciamento de Tickets

* `GET /tickets` - Retorna a listagem completa de tickets cadastrados.


* `GET /tickets/{ticket_id}` - Busca os detalhes de um ticket específico pelo ID.


* `POST /tickets` - Cria um novo ticket no sistema.


* **Payload esperado:**



```json
    {
      "titulo": "Erro no login",
      "descricao": "Usuário não consegue acessar o sistema."
    }
    ```
* `PATCH /tickets/{ticket_id}/status` - Atualiza parcialmente o status de um ticket existente.
  * **Payload esperado:**
```json
    {
      "status": "em andamento"
    }
    ```
* `DELETE /tickets/{ticket_id}` - Remove de forma definitiva um ticket do banco de dados.

---

## ⚙️ Configuração do Ambiente e Execução

### 1. Criar e Ativar o Ambiente Virtual (`venv`)

No diretório raiz do projeto, execute o comando correspondente ao seu sistema operacional:

```bash
# Criação do ambiente virtual
python -m venv .venv

```

* **No Windows (PowerShell):**

```powershell
  .\.venv\Scripts\Activate.ps1

```

* **No Windows (Prompt de Comando/CMD):**

```cmd
  .venv\Scripts\activate.bat

```

* **No Linux/macOS:**

```bash
  source .venv/bin/activate

```

### 2. Instalar as Dependências

```bash
pip install -r requirements.txt

```

### 3. Configurar as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto (utilize o padrão abaixo):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui

```

> ⚠️ **Importante:** O arquivo `.env` contém dados sensíveis e está devidamente configurado no seu `.gitignore` para nunca ser enviado ao controle de versão público.
> 
> 

### 4. Executar a Aplicação

Com o ambiente virtual ativo e o servidor do PostgreSQL devidamente rodando, inicialize a API com o Uvicorn:

```bash
uvicorn api.app:app --reload

```

---

## 📖 Documentação da API

A API conta com documentação interativa nativa gerada automaticamente a partir do código do FastAPI:

* **Swagger UI:** `http://127.0.0.1:8000/docs` (Permite testar os endpoints diretamente do navegador).


* **ReDoc:** `http://127.0.0.1:8000/redoc` (Documentação focada em leitura e especificação limpa).



---

## 🎯 Próximos Passos do Aprendizado

Com os objetivos da API com FastAPI concluídos, os próximos passos mapeados na trilha são:

* Implementar autenticação e controle de usuários (JWT).


* Melhorar o nível de abstração com Injeção de Dependências avançada.


* Integrar o sistema de tickets com fluxos de atendimento automatizados e inteligência artificial (Chatbots com histórico estruturado).


