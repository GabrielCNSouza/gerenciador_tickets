from typing import Protocol

from models.ticket import Ticket
from models.tickets_status import TicketStatus
from models.resultado_alteracao_status import ResultadoAlteracaoStatus


class TicketRepositoryProtocol(Protocol):

    def listar(self) -> list[Ticket]:
        ...

    def buscar_por_id(self, ticket_id: int) -> Ticket | None:
        ...

    def criar(self, titulo: str, descricao: str) -> Ticket | None:
        ...

    def alterar_status(self, ticket_id: int, novo_status: TicketStatus) -> ResultadoAlteracaoStatus:
        ...