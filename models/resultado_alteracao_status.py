from dataclasses import dataclass
from models.tickets_status import TicketStatus

@dataclass
class ResultadoAlteracaoStatus:
    sucesso: bool
    status_antigo: TicketStatus | None = None
    status_novo: TicketStatus | None = None