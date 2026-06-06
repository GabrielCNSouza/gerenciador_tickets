from models.ticket import Ticket
from models.tickets_status import TicketStatus
from models.resultado_operacao import ResultadoOperacao
from repositories.ticket_repository_protocol import TicketRepositoryProtocol

class TicketService:
    def __init__(self, repository: TicketRepositoryProtocol):
        self.repository = repository
    
    def criar_ticket(self, titulo: str, descricao: str) -> tuple[Ticket | None, ResultadoOperacao]:
        titulo = titulo.strip()
        descricao = descricao.strip()

        if not titulo:
            return None, ResultadoOperacao(
                sucesso=False,
                mensagem='O título não pode ficar vazio.'
            )

        if not descricao:
            return None, ResultadoOperacao(
                sucesso=False,
                mensagem='A descrição não pode ficar vazia.'
            )
        
        ticket = self.repository.criar(titulo=titulo, descricao=descricao)
        
        if not ticket:
            return None, ResultadoOperacao(
                sucesso=False,
                mensagem='Ticket não foi criado.'
            )
        
        return ticket, ResultadoOperacao(
            sucesso=True,
            mensagem=f'Ticket criado com sucesso! ID: {ticket.id}'
        )


    def listar_tickets(self) -> list[Ticket]:
        return self.repository.listar()
    

    def buscar_ticket_por_id(self, ticket_id: int) -> Ticket | None:
        return self.repository.buscar_por_id(ticket_id)
    

    def alterar_status(self, ticket_id: int, novo_status: TicketStatus) -> ResultadoOperacao:
        resultado = self.repository.alterar_status(ticket_id, novo_status)

        if not resultado.sucesso:
            return ResultadoOperacao(
                sucesso=False,
                mensagem='Ticket não encontrado.'
            )
        
        if resultado.status_antigo is None or resultado.status_novo is None:
            return ResultadoOperacao(
                sucesso=False,
                mensagem='Não foi possível identificar a alteração de status.'
            )
    
        if resultado.status_antigo == resultado.status_novo:
            return ResultadoOperacao(
                sucesso=False,
                mensagem = f'O ticket já está com o status "{novo_status.value}".'
            )

        return ResultadoOperacao(
            sucesso=True,
            mensagem=(
                f'Status alterado de '
                f'"{resultado.status_antigo.value}" para '
                f'"{resultado.status_novo.value}".'
            )
        )