from dataclasses import dataclass
from models.tickets_status import TicketStatus

@dataclass
class Ticket:
    id:int
    titulo:str
    descricao:str
    status:TicketStatus