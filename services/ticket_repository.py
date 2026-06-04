import json

from models.ticket import Ticket
from models.tickets_status import TicketStatus
from models.resultado_alteracao_status import ResultadoAlteracaoStatus


class TicketRepository:
    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo:str = caminho_arquivo
        self.tickets:list[Ticket] = []
        self.carregamento_ok:bool = False


    def carregar(self) -> None:
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, list):
                self.tickets = []
                self.carregamento_ok = False
                print('Sistema: o arquivo de tickets deve conter uma lista de tickets.')
                return

            self.tickets = []
            tickets_invalidos = []
            tickets_carregados = []

            for item in dados:
                if not isinstance(item, dict):
                    tickets_invalidos.append(
                        'ID desconhecido | Erro: item deve ser um objeto/dicionário'
                    )
                    continue

                try:
                    ticket_id = item.get("id", "desconhecido")
                    erros_tipo = self.validar_item(item)

                    if erros_tipo:
                        tickets_invalidos.append(
                            f'ID: {ticket_id} | Erro: {", ".join(erros_tipo)}'
                        )
                        continue

                    ticket = Ticket(
                        id=item['id'],
                        titulo=item['titulo'],
                        descricao=item['descricao'],
                        status=TicketStatus(item['status']) # busca o status entre as instancias da classe
                    )
                    tickets_carregados.append(ticket)
                
                except ValueError: 
                    tickets_invalidos.append(
                        f'ID: {ticket_id} | Erro: status inválido'
                    )

            if tickets_invalidos:
                self.tickets = []
                self.carregamento_ok = False
                print('Sistema: existem tickets inválidos no arquivo.')
                print(f'\nTickets inválidos não carregados: {len(tickets_invalidos)}')
                print(' ' + '\n '.join(map(str,tickets_invalidos)))
                print('\nSalvamento bloqueado para evitar perda de dados.')

                return
            
            self.tickets = tickets_carregados
            self.carregamento_ok = True

        except FileNotFoundError:
            self.tickets = []
            self.carregamento_ok = True

        except json.JSONDecodeError:
            self.tickets = []
            self.carregamento_ok = False
            print('Sistema: o arquivo de tickets está com JSON inválido. Salvamento bloqueado para evitar perda de dados.')
        

    def salvar(self) -> None:

        if not self.carregamento_ok:
            print('Sistema: salvamento bloqueado porque os dados não foram carregados corretamente.')
            return
        dados = []

        for ticket in self.tickets:
            dados.append({
                'id': ticket.id,
                'titulo': ticket.titulo,
                'descricao': ticket.descricao,
                'status': ticket.status.value
            })

        with open(self.caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)


    def listar(self) -> list[Ticket]:
        return self.tickets
    
    def buscar_por_id(self, ticket_id: int) -> Ticket | None:
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                return ticket
        return None


    def obter_proximo_id(self) -> int:
        if not self.tickets:
            return 1
        
        maior_id = 0

        for ticket in self.tickets:
            if ticket.id > maior_id:
                maior_id = ticket.id

        return maior_id + 1


    def validar_item(self, item: dict) -> list[str]:

        erros = []

        if 'id' not in item:
            erros.append('id é obrigatório')
        elif not isinstance(item.get('id'), int):
            erros.append('id deve ser um número inteiro')

        if 'titulo' not in item:
            erros.append('titulo é obrigatório')
        elif not isinstance(item.get('titulo'), str):
            erros.append('titulo deve ser um texto')

        if 'descricao' not in item:
            erros.append('descricao é obrigatória')
        elif not isinstance(item.get('descricao'), str):
            erros.append('descricao deve ser um texto')

        if 'status' not in item:
            erros.append('status é obrigatório')
        elif not isinstance(item.get('status'), str):
            erros.append('status deve ser um texto')
        
        return erros


    def criar(self, titulo: str, descricao: str) -> Ticket | None:

        if not self.carregamento_ok:
            print('Sistema: não é possível criar ticket porque os dados não foram carregados corretamente.')
            return None

        ticket = Ticket(
            id=self.obter_proximo_id(),
            titulo=titulo,
            descricao=descricao,
            status=TicketStatus.ABERTO
        )

        self.tickets.append(ticket)
        self.salvar()

        return ticket
    
    def alterar_status(self, ticket_id: int, novo_status: TicketStatus) -> ResultadoAlteracaoStatus:
        ticket = self.buscar_por_id(ticket_id)

        if not ticket:
            return ResultadoAlteracaoStatus(
                sucesso=False
            )
        
        status_antigo = ticket.status

        if status_antigo == novo_status:
            return ResultadoAlteracaoStatus(
                sucesso=True,
                status_antigo=status_antigo,
                status_novo=status_antigo
        )
        
        ticket.status = novo_status
        self.salvar()

        return ResultadoAlteracaoStatus(
            sucesso=True,
            status_antigo=status_antigo,
            status_novo=ticket.status
        )
